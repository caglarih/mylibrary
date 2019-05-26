import unittest
from io import StringIO
from unittest.mock import call, patch

from functions.kidega.product_query import (
    get_product_price,
    handler,
    parse_price_string,
    QUERY_TEMPLATE,
)

class ParsePriceStringTest(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        self.price_string = "25,20 ₺"
        self.price = 2520
        self.isbn = "ISBN"
        self.event = {
            "ISBN": self.isbn,
        }
        self.handler_response = {
            "price": self.price,
        }
        super().setUp(*args, **kwargs)

    def test_price_conversion(self):
        self.assertEqual(parse_price_string(self.price_string), self.price)

    @patch("urllib.request.urlopen")
    def test_get_product_price(self, urlopen_mock):
        self._mock_urlopen_responses(urlopen_mock)
        price = get_product_price(self.isbn)
        self._validate_urlopen_calls(urlopen_mock)
        self.assertEqual(price, self.price)

    @patch("urllib.request.urlopen")
    def test_handler(self, urlopen_mock):
        self._mock_urlopen_responses(urlopen_mock)
        response = handler(self.event, object())
        self._validate_urlopen_calls(urlopen_mock)
        self.assertEqual(response, self.handler_response)

    def _mock_urlopen_responses(self, urlopen_mock):
        urlopen_mock.side_effect = [
            StringIO(self._get_product_query_response()),
            StringIO(self._get_product_detail_response()),
        ]

    def _validate_urlopen_calls(self, urlopen_mock):
        urlopen_mock.assert_has_calls([
            call(QUERY_TEMPLATE % self.isbn),
            call("https://kidega.com/kitap/yuz-okuma-sanati-293295/detay"),
        ])

    def _get_content(self, file_name):
        with open("tests/resources/kidega/%s.html" % file_name, "r") as f:
            return f.read()

    def _get_product_query_response(self):
        return self._get_content("product_query")

    def _get_product_detail_response(self):
        return self._get_content("product_detail")

if __name__ == '__main__':
    unittest.main()
