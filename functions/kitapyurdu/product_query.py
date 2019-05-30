import re

from functions.base.product_query import AbstractBookExplorer


class KitapyurduBookExplorer(AbstractBookExplorer):

    QUERY_TEMPLATE = "https://www.kitapyurdu.com/index.php" \
        "?route=product/search&filter_name=%s"
    PRICE_XPATH = '//*[contains(@class, "price-sales")]/meta[1]'
    ISBN_LIST_XPATH = '//*[@id="product-table"]/div/div[15]/meta[1]'
    DETAIL_PAGE_XPATH = '//*[@id="product-table"]/div/div[3]/div/a'
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]\w+)).(?P<lower>([0-9]\w+))',
    )

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].attrib["content"]
