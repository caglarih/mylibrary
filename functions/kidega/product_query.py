from lxml import etree
import urllib


QUERY_TEMPLATE = "https://kidega.com/arama?query=%s"
DETAIL_PAGE_XPATH = '//*[@id="products"]/div/div/div[2]/div[1]/h4/a'
PRICE_XPATH = '/html/body/div[2]/div[1]/section/div/div/div[2]' \
    '/div[1]/div/div/div/div[1]/span[3]'


def parse_price_string(price_string):
    return int(float(price_string.replace(" ₺", "").replace(",", ".")) * 100)


def get_product_price(isbn):
    query_page = etree.parse(
        urllib.request.urlopen(QUERY_TEMPLATE % isbn),
        etree.HTMLParser(),
    )
    product_card = query_page.xpath(DETAIL_PAGE_XPATH)[0]
    detail_page_url = product_card.attrib["href"]
    detail_page = etree.parse(
        urllib.request.urlopen(detail_page_url),
        etree.HTMLParser(),
    )
    product_price = detail_page.xpath(PRICE_XPATH)[0].text.strip()
    return parse_price_string(product_price)


def handler(event, context):
    return {
        "price": get_product_price(event["ISBN"]),
    }
