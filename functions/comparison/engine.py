import unicodedata

from functions.product_query import (
    EXPLORERS,
    get_product_details,
    ProductQueryParameters,
)


__all__ = [
    "query_product",
]


def query_product(isbn, name):
    """Query prices of given isbn numbered book.

    :param isbn: ISBN number to get book info
    :type isbn: str
    :param name: Name of the product
    :type name: str
    :returns: Supplier to price map
    :rtype: dict
    """
    product_name = name.split("(")[0]
    params = ProductQueryParameters(isbn, product_name)
    price_map = {}
    for explorer in EXPLORERS:
        try:
            price_map[explorer.SUPPLIER] = explorer.get_product_price(params)
        except Exception as e:
            print(explorer.SUPPLIER, params.__dict__)
    return price_map
