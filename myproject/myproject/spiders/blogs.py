import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import BlogPost


class BlogsSpider(CrawlSpider):
    name = 'blogs'
    # どこまで辿るか
    # allowed_domains = ['b.hatena.ne.jp/hotentry/it']
    start_urls = (
        # はてなブックマーク(テクノロジ)新着
        'http://b.hatena.ne.jp/hotentry/it',
        # Qiita新着
        'https://qiita.com/',
    )

    rules = (
        # はてなブログの記事ページの正規表現(外部まで追わない)
        Rule(LinkExtractor(allow=r'/entry/\d+/'), callback='parse_hatena'),    
        # Qiita新着の記事ページの正規表現
        Rule(LinkExtractor(allow=r'/items/\w+/'), callback='parse_qiita'),  
        #     r'/archives/\d+\.html$',  # ライブドアブログの記事ページの正規表現
        #     r'/@\w+/[^/]+',           # Mediumの記事ページの正規表現
        # ), deny=(
        #     r'^https?://b\.hatena\.ne\.jp/',  # クロールしない
        # )
    )

    custom_settings = {
        # リンクを辿る深さを1に制限する
        'DEPTH_LIMIT': 1,
        # ドメイン単位ではなくIPアドレス単位でウェイトを入れる
        'CONCURRENT_REQUESTS_PER_IP': 8,
    }

    def parse_hatena(self, response):
        # トピックスのページからタイトルと本文を抜き出す。
        item = BlogPost()
        #entry-26006613795082668 > div > header > h1 > a
        item['title'] = response.css('header > h1 > a::text').extract_first()
        #entry-26006613795082668 > div > div > p:nth-child(1)
        item['body']  = response.css('div > div > p::text').extract_first()
        item['url'] = response.url
        yield item

    def parse_qiita(self, response):
        # トピックスのページからタイトルと本文を抜き出す。
        item = BlogPost()
        #PersonalArticlePage-react-component-4d7e845a-d1af-4b63-b8e1-7a1932580ce3 > div.p-items_wrapper > div > div.p-items_main > div:nth-child(1) > div.css-8qb8m4 > h1
        item['title'] = response.css('h1::text').extract_first()
        #personal-public-article-body
        item['body']  = response.css('personal-public-article-body::text').extract_first()
        item['url'] = response.url
        yield item