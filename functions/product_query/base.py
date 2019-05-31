import abc
from collections import namedtuple

import requests
from lxml import html


__all__ = [
    "AbstractBookExplorer",
    "ProductQueryParameters",
]


ProductQueryParameters = namedtuple(
    "ProductQueryParameters",
    "isbn10 isbn13 name",
)

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'


class AbstractBookExplorer(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def VENDOR():
        raise NotImplementedError

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
    def get_product_price(cls, query_parameters):
        detail_page_url = cls._get_detail_page_url(query_parameters)
        response = requests.get(
            detail_page_url,
            headers={
                "User-Agent": USER_AGENT,
            },
        )
        detail_page = html.fromstring(response.content)
        product_price = cls._get_price_string(detail_page)
        return cls._parse_price_string(product_price)

    @classmethod
    def _parse_price_string(cls, price_string):
        group = cls.PRICE_STRING_RE.match(price_string).groupdict()
        upper = int(group["upper"])
        lower = int(group["lower"])
        return upper * 100 + lower
