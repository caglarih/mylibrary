import re

from functions.product_query.base import AbstractBookExplorer, BookDetails
from utils import book_suppliers, tree_utils


__all__ = [
    "KidegaBookExplorer",
]


QUERY_TEMPLATE = "https://kidega.com/arama?query=%s"
DETAIL_PAGE_XPATH = '//*[@id="products"]/div/div/div[2]/div[1]/h4/a'
DETAIL_BOX_XPATH = "//div[@class='productInfo']/div[2]/div"
BOXED_DETAIL_FIELDS = {
    "ISBN:": ("isbn", str),
    "Kapak:": ("cover", str),
    "Boyut:": ("size", str),
    "Sayfa Sayısı:": ("page_count", int),
}
INDIVIDUAL_DETAIL_FIELDS = {
    "name": "//h1[@class='book-detail-title']",
    "author": "//a[@class='book-author']/b",
    "publisher": "//a[@class='publisher']",
}


class KidegaBookExplorer(AbstractBookExplorer):

    SUPPLIER = book_suppliers.Supplier.KIDEGA
    PRICE_STRING_RE = re.compile(
        r'(?P<upper>([0-9]+)),(?P<lower>([0-9]+)) ₺',
    )

    @classmethod
    def _get_detail_page_url(cls, query_parameters):
        query_url = QUERY_TEMPLATE % query_parameters.isbn
        query_page = tree_utils.create_from_url(query_url)
        product_card = query_page.xpath(DETAIL_PAGE_XPATH)[0]
        return product_card.attrib["href"]

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath("//span[@class='f26b']")[0].text.strip()

    @classmethod
    def get_product_details(cls, query_parameters):
        """Get book details.

        :param query_parameter: parameters to query a book
        :type query_parameters: functions.product_query.ProductQueryParameters
        :returns: A dataclass with book information
        :rtype:functions.product_query.BookDetails
        """
        details_url = cls._get_detail_page_url(query_parameters)
        detail_page = tree_utils.create_from_url(details_url)
        details = {
            key: detail_page.xpath(xpath)[0].text
            for key, xpath in INDIVIDUAL_DETAIL_FIELDS.items()
        }
        for detail_container in detail_page.xpath(DETAIL_BOX_XPATH):
            field, value = detail_container.getchildren()[:2]
            detail_field = BOXED_DETAIL_FIELDS.get(field.text)
            if detail_field:
                field_name, sanitizer = detail_field
                details[field_name] = sanitizer(value.text)
        return BookDetails(**details)
