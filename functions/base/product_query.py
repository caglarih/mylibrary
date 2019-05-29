import abc

from lxml import etree
from urllib import request, parse


class AbstractBookExplorer(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def QUERY_TEMPLATE():
        raise NotImplementedError

    @abc.abstractproperty
    def DETAIL_PAGE_XPATH():
        raise NotImplementedError

    @abc.abstractproperty
    def PRICE_XPATH():
        raise NotImplementedError

    @abc.abstractproperty
    def PRICE_STRING_RE():
        raise NotImplementedError

    @classmethod
    def get_product_price(cls, isbn, product_name=None):
        detail_page_url = cls._get_detail_url_from_isbn(isbn) \
            if product_name is None \
            else cls._get_detail_url_with_product_name(isbn, product_name)
        detail_page = etree.parse(
            request.urlopen(detail_page_url),
            etree.HTMLParser(),
        )
        product_price = detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()
        return cls._parse_price_string(product_price)

    @classmethod
    def _get_detail_url_from_isbn(cls, isbn):
        query_page = etree.parse(
            request.urlopen(cls.QUERY_TEMPLATE % isbn),
            etree.HTMLParser(),
        )
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        return product_card.attrib["href"]

    @classmethod
    def _get_detail_url_with_product_name(cls, isbn, product_name):
        query_page = etree.parse(
            request.urlopen(cls.QUERY_TEMPLATE % parse.quote(product_name)),
            etree.HTMLParser(),
        )
        for product in query_page.xpath(cls.PRODUCT_LIST_XPATH):
            print(product.xpath(cls.PRODUCT_ISBN_XPATH))
            isbn_container = product.xpath(cls.PRODUCT_ISBN_XPATH)[0]
            if isbn_container.attrib["content"] == isbn:
                print(product.xpath(cls.PRODUCT_DETAIL_XPATH)[0].attrib["href"])
                return product.xpath(cls.PRODUCT_DETAIL_XPATH)[0].attrib["href"]

    @classmethod
    def handler(cls, event, context):
        return {
            "price": cls.get_product_price(event["ISBN"]),
        }

    @classmethod
    def _parse_price_string(cls, price_string):
        group = cls.PRICE_STRING_RE.match(price_string).groupdict()
        upper = int(group["upper"])
        lower = int(group["lower"])
        return upper * 100 + lower
