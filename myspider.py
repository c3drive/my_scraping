import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    # クロールを開始する URL のリスト
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response):
        """
        トップページから各ブログへのリンクを抜き出してたどる
        """
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)
