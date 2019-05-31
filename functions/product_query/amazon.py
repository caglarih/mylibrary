import re

import requests
from lxml import html

from functions.product_query.base import AbstractBookExplorer


__all__ = [
    "AmazonBookExplorer",
]


class AmazonBookExplorer(AbstractBookExplorer):

    VENDOR = "Amazon"
    QUERY_TEMPLATE = "https://www.amazon.com.tr/s?k=%s"
    DETAIL_PAGE_XPATH = '//*[@id="search"]/div[1]/div[2]/div/span[3]/div[1]' \
        '/div[1]/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/h2/a'
    PRICE_XPATH = '//*[@id="buyNewSection"]/div/div/span/span'
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]\w+)),(?P<lower>([0-9]\w+)) TL',
    )

    @classmethod
    def _get_detail_page_url(cls, query_parameters):
        query_page_content = cls._get_query_page(query_parameters)
        query_page = html.fromstring(query_page_content)
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        return "https://www.amazon.com.tr%s" % product_card.attrib["href"]

    @classmethod
    def _get_query_page(cls, query_parameters):
        response = requests.get(cls.QUERY_TEMPLATE % query_parameters.isbn13)
        if response.status_code == 200:
            return response.content
        else:
            raise ValueError("Non-200 response from amazon")

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()
