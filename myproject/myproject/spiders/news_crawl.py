import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myproject.items import Headline


class NewsCrawlSpider(CrawlSpider):
    # Spider の名前
    name = 'news_crawl'
    # クロール対象とするドメインのリスト
    allowed_domains = ['news.yahoo.co.jp']
    # クロールを開始する URL のリスト。
    start_urls = (
        'https://news.yahoo.co.jp/topics/it',
    )

    # リンクを辿るルールのリスト
    rules = (
        # トピックスのページへのリンクを辿り、レスポンスをparse_topics()メソッドで処理する
        Rule(LinkExtractor(allow=r'/pickup/\d+$'), callback='parse_topics'),
    )

    #def parse(self, response):
    #    pass
    # def parse(self, response):
    #     # トップページのトピックス一覧から個々のトピックスへのリンクを抜き出して表示する。
    #     for url in response.css('ul.newsFeed_list a::attr("href")').re(r'/pickup/\d+$'):
    #         yield scrapy.Request(response.urljoin(url), self.parse_topics)

    def parse_topics(self, response):
        # トピックスのページからタイトルと本文を抜き出す。
        item = Headline()
        item['title'] = response.css('#uamods-pickup > div.sc-keIums.euBSAz > a > p::text').extract_first()
        item['body']  = response.css('#uamods-pickup > div.sc-keIums.euBSAz > p::text').extract_first()
        item['url'] = response.url
        yield item