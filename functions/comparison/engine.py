import unicodedata

from functions.product_query import (
    EXPLORERS,
    get_product_details,
    ProductQueryParameters,
)


def query_product(isbn):
    params = ProductQueryParameters(isbn, None)
    details = get_product_details(params)
    product_name = unicodedata.normalize(
        "NFKD",
        "%s %s" % (details["author"], details["name"]),
    ).encode("ascii", "ignore")
    params = ProductQueryParameters(details["isbn"], product_name)
    return {
        explorer.SUPPLIER: explorer.get_product_price(params)
        for explorer in EXPLORERS
    }
