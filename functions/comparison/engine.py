from functions.product_query import EXPLORERS, ProductQueryParameters


def query_product(isbn, name):
    params = ProductQueryParameters(isbn, name)
    return {
        explorer.VENDOR: explorer.get_product_price(params)
        for explorer in EXPLORERS
    }
