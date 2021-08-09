import scrapy

from myproject.items import Headline


class NewsSpider(scrapy.Spider):
    # Spider の名前
    name = 'news'
    # クロール対象とするドメインのリスト
    allowed_domains = ['news.yahoo.co.jp']
    # クロールを開始する URL のリスト。
    start_urls = (
        'https://news.yahoo.co.jp/topics/it',
    )

    def parse(self, response):
        # トップページのトピックス一覧から個々のトピックスへのリンクを抜き出して表示する。
        for url in response.css('ul.newsFeed_list a::attr("href")').re(r'/pickup/\d+$'):
            yield scrapy.Request(response.urljoin(url), self.parse_topics)

    def parse_topics(self, response):
        # トピックスのページからタイトルと本文を抜き出す。
        item = Headline()
        item['title'] = response.css('#uamods-pickup > div.sc-keIums.euBSAz > a > p::text').extract_first()
        item['body']  = response.css('#uamods-pickup > div.sc-keIums.euBSAz > p::text').extract_first()
        item['url'] = response.url
        yield item