# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    """
    ニュースヘッドラインを表すItem
    """
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()


class BlogPost(scrapy.Item):
    """
    ブログItem
    """
    title = scrapy.Field()
    body = scrapy.Field()
    url = scrapy.Field()


class Page(scrapy.Item):
    """
    Webページ
    """
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

    def __repr__(self):
        """
        ログへの出力時に長くなり過ぎないよう、contentを省略する。
        """

        p = Page(self)  # このPageを複製したPageを得る。
        if len(p['content']) > 100:
            p['content'] = p['content'][:100] + '...'  # 100文字より長い場合は省略する。

        return super(Page, p).__repr__()  # 複製したPageの文字列表現を返す。
        

class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

