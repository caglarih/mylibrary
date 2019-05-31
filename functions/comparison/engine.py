from functions.product_query import EXPLORERS, ProductQueryParameters


def query_product(isbn10, isbn13, name):
    params = ProductQueryParameters(isbn10, isbn13, name)
    return {
        explorer.VENDOR: explorer.get_product_price(params)
        for explorer in EXPLORERS
    }
