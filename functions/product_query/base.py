import abc
from dataclasses import dataclass

from utils import tree_utils

import requests
from lxml import html


__all__ = [
    "AbstractBookExplorer",
    "BookDetails",
    "ProductQueryParameters",
]


@dataclass
class ProductQueryParameters:
    isbn: str
    name: str = None


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'


@dataclass
class BookDetails:
    isbn: str
    cover: str
    size: str
    page_count: int
    name: str
    author: str
    publisher: str



class AbstractBookExplorer(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractproperty
    def SUPPLIER():
        raise NotImplementedError

    @staticmethod
    @abc.abstractproperty
    def PRICE_STRING_RE():
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _get_price_string(cls, detail_page):
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def _get_detail_page_url(cls, detail_page):
        raise NotImplementedError

    @classmethod
    def get_product_price(cls, query_parameters):
        detail_page_url = cls._get_detail_page_url(query_parameters)
        detail_page = tree_utils.create_from_url(detail_page_url)
        product_price = cls._get_price_string(detail_page)
        return cls._parse_price_string(product_price)

    @classmethod
    def _parse_price_string(cls, price_string):
        group = cls.PRICE_STRING_RE.match(price_string).groupdict()
        upper = int(group["upper"])
        lower = int(group["lower"])
        return upper * 100 + lower
