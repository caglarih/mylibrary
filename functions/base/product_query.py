import abc

from lxml import etree
from urllib import request


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
    def get_product_price(cls, isbn):
        query_page = etree.parse(
            request.urlopen(cls.QUERY_TEMPLATE % isbn),
            etree.HTMLParser(),
        )
        product_card = query_page.xpath(cls.DETAIL_PAGE_XPATH)[0]
        detail_page_url = product_card.attrib["href"]
        detail_page = etree.parse(
            request.urlopen(detail_page_url),
            etree.HTMLParser(),
        )
        product_price = detail_page.xpath(cls.PRICE_XPATH)[0].text.strip()
        return cls._parse_price_string(product_price)

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
