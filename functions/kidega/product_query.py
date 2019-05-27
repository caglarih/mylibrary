import re

from functions.base.product_query import AbstractBookExplorer


class KidegaBookExplorer(AbstractBookExplorer):

    QUERY_TEMPLATE = "https://kidega.com/arama?query=%s"
    DETAIL_PAGE_XPATH = '//*[@id="products"]/div/div/div[2]/div[1]/h4/a'
    PRICE_XPATH = '/html/body/div[2]/div[1]/section/div/div/div[2]' \
        '/div[1]/div/div/div/div[1]/span[3]'
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]\w+)),(?P<lower>([0-9]\w+)) ₺',
    )
