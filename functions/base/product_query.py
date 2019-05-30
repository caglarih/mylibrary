import abc

import requests
from lxml import html
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
        detail_page = html.fromstring(
            requests.get(detail_page_url).content,
        )
        product_price = cls._get_price_string(detail_page)
        return cls._parse_price_string(product_price)

    @classmethod
    def _get_detail_url_from_isbn(cls, isbn):
        print(cls.QUERY_TEMPLATE % cls._sanitize_isbn(isbn))
        query_page = html.fromstring(
            requests.get(cls.QUERY_TEMPLATE % cls._sanitize_isbn(isbn)).content,
        )
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        return product_card.attrib["href"]

    @classmethod
    def _get_detail_url_with_product_name(cls, isbn, product_name):
        query_page = html.fromstring(
            requests.get(cls.QUERY_TEMPLATE % parse.quote(product_name)).content,
        )
        for index, isbn_container in enumerate(query_page.xpath(cls.ISBN_LIST_XPATH)):
            if isbn_container.attrib["content"] in isbn:
                anchor = query_page.xpath(cls.DETAIL_PAGE_XPATH)[index]
                return anchor.attrib["href"].encode("utf-8").decode("utf-8")

    @classmethod
    def handler(cls, event, context):
        return {
            "price": cls.get_product_price(event["ISBN"]),
        }

    @classmethod
    def _get_price_string(cls, detail_page):
        return detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()

    classmethod
    def _sanitize_isbn(cls, isbn):
        return isbn

    @classmethod
    def _parse_price_string(cls, price_string):
        group = cls.PRICE_STRING_RE.match(price_string).groupdict()
        upper = int(group["upper"])
        lower = int(group["lower"])
        return upper * 100 + lower
