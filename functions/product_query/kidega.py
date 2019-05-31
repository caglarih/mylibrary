import re

import requests
from lxml import html

from functions.product_query.base import AbstractBookExplorer


__all__ = [
    "KidegaBookExplorer",
]


class KidegaBookExplorer(AbstractBookExplorer):

    VENDOR = "Kidega"
    QUERY_TEMPLATE = "https://kidega.com/arama?query=%s"
    DETAIL_PAGE_XPATH = '//*[@id="products"]/div/div/div[2]/div[1]/h4/a'
    PRICE_XPATH = '/html/body/div[2]/div[1]/section/div/div/div[2]' \
        '/div[1]/div/div/div/div[1]/span[3]'
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]\w+)),(?P<lower>([0-9]\w+)) ₺',
    )

    @classmethod
    def _get_detail_page_url(cls, query_parameters):
        query_page = html.fromstring(
            requests.get(
                cls.QUERY_TEMPLATE % query_parameters.isbn13,
            ).content,
        )
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        return product_card.attrib["href"]

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()
