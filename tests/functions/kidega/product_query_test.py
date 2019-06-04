import unittest
from io import StringIO
from unittest.mock import call, patch

from functions.product_query import (
    BookDetails,
    KidegaBookExplorer,
    ProductQueryParameters,
)


EXPECTED_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit"
    "/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}


class KidegaBookExplorerTest(unittest.TestCase):

    def setUp(self, *args, **kwargs):
        self.price_string = "28,54 ₺"
        self.price = 2854
        self.isbn = "ISBN"
        self.parameters = ProductQueryParameters(self.isbn, None)
        self.details = BookDetails(
            self.isbn,
            "Ciltsiz",
            "Normal",
            284,
            "Yüz Okuma Sanatı",
            "Murat Kaplan",
            "Ayzıt Yayınları",
        )
        super().setUp(*args, **kwargs)

    def test_price_conversion(self):
        self.assertEqual(
            KidegaBookExplorer._parse_price_string(self.price_string),
            self.price,
        )

    @patch("requests.get")
    def test_get_product_price(self, requests_get_mock):
        self._mock_requests_responses(requests_get_mock)
        price = KidegaBookExplorer.get_product_price(self.parameters)
        self._validate_requests_calls(requests_get_mock)
        self.assertEqual(price, self.price)

    @patch("requests.get")
    def test_get_product_details(self, requests_get_mock):
        self._mock_requests_responses(requests_get_mock)
        details = KidegaBookExplorer.get_product_details(self.parameters)
        self._validate_requests_calls(requests_get_mock)
        self.assertEqual(details, self.details)

    def _mock_requests_responses(self, requests_get_mock):
        requests_get_mock.side_effect = [
            self._get_product_query_response(),
            self._get_product_detail_response(),
        ]

    def _validate_requests_calls(self, requests_get_mock):
        requests_get_mock.assert_has_calls([
            call(
                KidegaBookExplorer.QUERY_TEMPLATE % self.isbn,
                headers=EXPECTED_HEADERS,
            ),
            call(
                "https://kidega.com/kitap/yuz-okuma-sanati-293295/detay",
                headers=EXPECTED_HEADERS,
            ),
        ])

    def _get_product_query_response(self):
        return self._generate_response("product_query")

    def _get_product_detail_response(self):
        return self._generate_response("product_detail")

    def _generate_response(self, file_name):
        return self._make_requests_response(self._get_content(file_name))

    def _get_content(self, file_name):
        with open("tests/resources/kidega/%s.html" % file_name, "r") as f:
            return f.read()

    def _make_requests_response(self, content):
        mocked_response = unittest.mock.Mock()
        mocked_response.status_code = 200
        mocked_response.content = content
        return mocked_response

if __name__ == '__main__':
    unittest.main()
