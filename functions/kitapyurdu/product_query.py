import re

from functions.base.product_query import AbstractBookExplorer


class KitapyurduBookExplorer(AbstractBookExplorer):

    QUERY_TEMPLATE = "https://www.kitapyurdu.com/index.php" \
        "?route=product/search&filter_name=%s"
    DETAIL_PAGE_XPATH = '//*[@id="products"]/div/div/div[2]/div[1]/h4/a'
    PRICE_XPATH = '/html/body/div[2]/div[1]/section/div/div/div[2]' \
        '/div[1]/div/div/div/div[1]/span[3]'
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]\w+)),(?P<lower>([0-9]\w+)) ₺',
    )
    PRODUCT_LIST_XPATH = '//*[@id="product-table"]/div'
    PRODUCT_DETAIL_XPATH = '/div[1]/div[1]/div/a'
    PRODUCT_ISBN_XPATH = 'div[2]/div'
