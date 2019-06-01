import re

from functions.product_query.base import AbstractBookExplorer
from utils import tree_utils


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
        r'(?P<upper>([0-9]+)),(?P<lower>([0-9]+)) TL',
    )

    @classmethod
    def _get_detail_page_url(cls, query_parameters):
        query_page = cls._get_query_page(query_parameters)
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        return "https://www.amazon.com.tr%s" % (
            "/".join(
                product_card.attrib["href"].split("/")[:4]
            ),
        )

    @classmethod
    def _get_query_page(cls, query_parameters):
        query_url = cls.QUERY_TEMPLATE % query_parameters.isbn
        return tree_utils.create_from_url(query_url)

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()
