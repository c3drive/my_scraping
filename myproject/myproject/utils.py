import logging

import lxml.html
from readability import Document

# ReadabilityのDEBUG/INFOレベルのログを表示しないようにする。
logging.getLogger('readability.readability').setLevel(logging.WARNING)


def get_content(html):
    """
    HTMLの文字列から (タイトル, 本文) のタプルを取得する。
    """

    document = Document(html)
    content_html = document.summary()
    # HTMLタグを除去して本文のテキストのみを取得する。
    content_text = lxml.html.fromstring(content_html).text_content().strip()
    short_title = document.short_title()

    return short_title, content_text