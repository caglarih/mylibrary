import re

import requests
from lxml import html
from urllib import parse

from functions.product_query.base import AbstractBookExplorer


__all__ = [
    "KitapyurduBookExplorer",
]


class KitapyurduBookExplorer(AbstractBookExplorer):

    VENDOR = "KitapYurdu"
    QUERY_TEMPLATE = "https://www.kitapyurdu.com/index.php" \
        "?route=product/search&filter_name=%s"
    PRICE_XPATH = '//*[contains(@class, "price-sales")]/meta[1]'
    ISBN_LIST_XPATH = '//*[@id="product-table"]/div/div[15]/meta[1]'
    DETAIL_PAGE_XPATH = '//*[@id="product-table"]/div/div[3]/div/a'
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]+)).(?P<lower>([0-9]+))',
    )

    @classmethod
    def _get_detail_page_url(cls, query_parameters):
        query_url = cls.QUERY_TEMPLATE % parse.quote(query_parameters.name)
        query_page = html.fromstring(requests.get(query_url).content)
        for index, isbn_container in enumerate(query_page.xpath(cls.ISBN_LIST_XPATH)):
            if isbn_container.attrib["content"] in query_parameters.isbn:
                anchor = query_page.xpath(cls.DETAIL_PAGE_XPATH)[index]
                return anchor.attrib["href"]

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].attrib["content"]
