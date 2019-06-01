from functions.product_query.base import *
from functions.product_query.amazon import AmazonBookExplorer
from functions.product_query.kidega import KidegaBookExplorer
from functions.product_query.kitapyurdu import KitapyurduBookExplorer


EXPLORERS = [
    AmazonBookExplorer,
    KidegaBookExplorer,
    KitapyurduBookExplorer,
]


get_product_details = KidegaBookExplorer.get_product_details
