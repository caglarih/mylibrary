import unicodedata

from functions.product_query import (
    EXPLORERS,
    get_product_details,
    ProductQueryParameters,
)


__all__ = [
    "query_product",
]


def query_product(isbn):
    """Query prices of given isbn numbered book.

    :param isbn: ISBN number to get book info
    :type isbn: str
    :returns: Supplier to price map
    :rtype: dict
    """
    params = ProductQueryParameters(isbn)
    details = get_product_details(params)
    product_name = unicodedata.normalize(
        "NFKD",
        "%s %s" % (details.author, details.name),
    ).encode("ascii", "ignore")
    params = ProductQueryParameters(details.isbn, product_name)
    return {
        explorer.SUPPLIER: explorer.get_product_price(params)
        for explorer in EXPLORERS
    }
