import re

from functions.product_query.base import AbstractBookExplorer
from utils import tree_utils


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
        r'(?P<upper>([0-9]+)),(?P<lower>([0-9]+)) ₺',
    )

    @classmethod
    def _get_detail_page_url(cls, query_parameters):
        query_url = cls.QUERY_TEMPLATE % query_parameters.isbn
        query_page = tree_utils.create_from_url(query_url)
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        return product_card.attrib["href"]

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()


    @classmethod
    def get_product_details(cls, query_parameters):
        details_url = cls._get_detail_page_url(query_parameters)
        detail_page = tree_utils.create_from_url(details_url)
        price = cls._parse_price_string(
            cls._get_price_string(detail_page),
        )
        name = detail_page.xpath(
            '/html/body/div[2]/div[1]/section/div/div/div[1]/div/div[2]/div[1]/h1',
        )[0].text
        author = detail_page.xpath(
            '/html/body/div[2]/div[1]/section/div/div/div[1]/div/div[2]/div[1]/a[1]/b',
        )[0].text
        page_count = detail_page.xpath(
            '/html/body/div[2]/div[1]/section/div/div/div[2]/div[3]/div[2]/div[6]/span',
        )[0].text
        return {
            "isbn": query_parameters.isbn,
            "name": name,
            "author": author,
            "page_count": int(page_count),
        }
