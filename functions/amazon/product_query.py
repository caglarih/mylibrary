import re

from functions.base.product_query import AbstractBookExplorer


class AmazonBookExplorer(AbstractBookExplorer):

    QUERY_TEMPLATE = "https://www.amazon.com.tr/s?k=%s"
    DETAIL_PAGE_XPATH = '//*[@id="result_0"]/div/div/div/div[1]/div/div/a'
    PRICE_XPATH = '//*[@id="buyNewSection"]/div/div/span/span'
    PRICE_STRING_RE = re.compile(r'(?P<upper>([0-9]\w+)),(?P<lower>([0-9]\w+)) TL')

    @classmethod
    def _sanitize_isbn(cls, isbn):
        return isbn.replace("-", "")
