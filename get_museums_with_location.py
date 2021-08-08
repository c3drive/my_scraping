import time
import sys
import os
import json
import dbm
from urllib.request import urlopen
from urllib.parse import urlencode
from SPARQLWrapper import SPARQLWrapper

def main():
    features = []
    for museum in get_museums():
        label = museum.get('label', museum['s'])
        address = museum['address']

        if 'lon_degree' in museum:
            # 位置情報が含まれる場合は、経度と緯度を60進数（度分秒）から10進数に変換する。
            # 10進数の度 = 60進数の度 + 60進数の分 / 60 + 60進数の秒 / 3600
            lon = float(museum['lon_degree']) + float(museum['lon_minute']) / 60 + \
                float(museum['lon_second']) / 3600
            lat = float(museum['lat_degree']) + float(museum['lat_minute']) / 60 + \
                float(museum['lat_second']) / 3600
        else:
            # 位置情報が含まれない場合は、住所をジオコーディングして経度と緯度を取得する。
            lon, lat = geocode(address)
        
        print(label, address, lon, lat)
        if lon is None:
            continue
        
        # featuresに美術館の情報をGeoJSON Feature 形式で追加する
        features.append({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
            'properties': {'label': label, 'address': address},
        })

    # GeoJSON FeatureCollection 형식으로 dict를 생성합니다.
    feature_collection = {
        'type': 'FeatureCollection',
        'features': features,
    }
    # FeatureCollection을 .geojson이라는 확장자의 파일로 저장합니다.
    with open('museums.geojson', 'w') as f:
        json.dump(feature_collection, f)

def get_museums():
    """
    SPARQL을 사용해 DBpedia에서 박물관 정보 추출하기
    """
    print('Executing SPARQL query...', file=sys.stderr)
    
    # SPARQL 엔드 포인트를 지정해서 인스턴스를 생성합니다.
    sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    
    # 한국의 박물관을 추출하는 쿼리입니다..
    #sparql.setQuery(r'''
    # SELECT * WHERE {
    #     ?s rdf:type dbpedia-owl:Museum2 .
    #     ?s prop-ja:所在地 ?address .
    #     OPTIONAL {
    #         ?s prop-ja:経度度 ?lon_degree;
    #          ?s rdfs:label ?label . }
    # } ORDER BY ?s
    # ''')
    #sparql = SPARQLWrapper('http://ja.dbpedia.org/sparql')
    # 日本の美術館を取得するクエリを設定する。バックスラッシュを含むので、rで始まるraw文字列を使用している。
    sparql.setQuery(r'''
    PREFIX dbpedia-owl:  <http://dbpedia.org/ontology/> 
    SELECT * WHERE {
        ?s rdf:type dbpedia-owl:Museum ;
        prop-ja:所在地 ?address .
        OPTIONAL { ?s rdfs:label ?label . }
        OPTIONAL {
        ?s prop-ja:経度度 ?lon_degree ;
            prop-ja:経度分 ?lon_minute ;
            prop-ja:経度秒 ?lon_second ;
            prop-ja:緯度度 ?lat_degree ;
            prop-ja:緯度分 ?lat_minute ;
            prop-ja:緯度秒 ?lat_second .
        }
        FILTER REGEX(?address, "^\\p{Han}{2,3}[都道府県]")
    } ORDER BY ?s
    ''')

    # 반환 형식을 JSON으로 지정합니다.
    sparql.setReturnFormat('json')
    print(sparql)
    # query()로 쿼리를 실행한 뒤 convert()로 파싱합니다.
    response = sparql.query().convert()
    print('Got {0} results'.format(len(response['results']['bindings']), file=sys.stderr))
    # 쿼리 결과를 반복 처리합니다.
    for result in response['results']['bindings']:
        # 다루기 쉽게 dict 형태로 변환해서 yield합니다.
        yield {name: binding['value'] for name, binding in result.items()}



# Yahoo Geolocation API
YAHOO_GEOCODER_API_URL = 'http://geo.search.olp.yahooapis.jp/OpenLocalPlatform/V1/geoCoder'


# Google Geolocation API
GOOGLE_GEOCODER_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
geocoding_cache = dbm.open('geocoding.db', 'c')

def geocode(address):
    """
    매개변수로 지정한 주소를 지오코딩해서 위도와 경도를 반환합니다.
    """
    if address not in geocoding_cache:
        # 주소가 캐시에 존재하지 않는 경우 지오코딩합니다.
        print('Geocoding {0}...'.format(address), file=sys.stderr)
        time.sleep(1)
        # url = GOOGLE_GEOCODER_API_URL + '?' + urlencode({
        #     'key': os.environ['GOOGLE_API_ID'],
        #     'language': 'ja',
        #     'address': address,
        # })
        url = YAHOO_GEOCODER_API_URL + '?' + urlencode({
            'appid': os.environ['YAHOOJAPAN_APP_ID'],
            'output': 'json',
            'address': address,
        })
        response_text = urlopen(url).read()
        # API 응답을 캐시에 저장합니다.
        # 문자열을 키와 값에 넣으면 자동으로 bytes로 변환합니다.
        geocoding_cache[address] = response_text
    
    # 캐시 내의 API 응답을 dict로 변환합니다.
    # 값은 bytes 자료형이므로 문자열로 변환합니다.
    response = json.loads(geocoding_cache[address].decode('utf-8'))
    try:
        # JSON 형식에서 값을 추출합니다.
        lng = response['results'][0]['geometry']['location']['lng']
        lat = response['results'][0]['geometry']['location']['lat']
        # float 형태로 변환한 뒤 튜플을 반환합니다.
        return (float(lng), float(lat))
    except:
        return (None, None)

if __name__ == '__main__':
    main()