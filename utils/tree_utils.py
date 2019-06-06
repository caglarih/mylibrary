import random
import time

import requests
from lxml import html
import user_agent


headers = {
    "Accept": "text/html,application/xhtml+xml,application"
    "/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "tr-TR,tr;q=0.8",
}


def create_from_url(url, max_retry=3, current_retry=0):
    response = requests.get(
        url,
        headers={"User-Agent": user_agent.generate_user_agent(), **headers},
    )
    if response.status_code == 200:
        return html.fromstring(response.content)
    if response.status_code in {503, 429}:
        if current_retry < max_retry:
            time.sleep(random.random())
            create_from_url(url, max_retry, current_retry + 1)
