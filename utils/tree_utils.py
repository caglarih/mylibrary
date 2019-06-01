import random
import time

import requests
from lxml import html


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' \
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'


def create_from_url(url, max_retry=3, current_retry=0):
    response = requests.get(url, headers={"User-Agent": USER_AGENT})
    if response.status_code == 200:
        return html.fromstring(response.content)
    if response.status_code in {503, 429}:
        if current_retry < max_retry:
            time.sleep(random.random())
            create_from_url(url, max_retry, current_retry + 1)
