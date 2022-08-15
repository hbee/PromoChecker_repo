from typing import Dict, Tuple
import json

import requests
from bs4 import BeautifulSoup


url_link = "https://www.asos.com/fr/asos-design/asos-design-short-de-bain-mi-long-noir/prd/201352106?clr=noir&colourWayId=201352107&cid=13210"

def get_item_data(url: str) -> Tuple[str, float]:
    """parses an item's web page and extract relevant information

    Args:
        url (str): url link to the item web page

    Returns:
        name, price (Tuple): name of the product, its price, and url for its image
    """

    headers: Dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Accept-Languages": "en-GB, en-US, fr"
    }

    response: requests.Response = requests.get(url, headers=headers)
    page_parsed = BeautifulSoup(response.text, "lxml")
    product_data: str = json.loads(
        page_parsed.find('script', type='application/ld+json').string
    )

    name: str = product_data['name']

    price_endpoint: str = (
        f"https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={product_data['productID']}&store=FR&currency=EUR"
    )
    product_price_info: Dict = requests.get(
        price_endpoint, headers=headers).json()[0]
    price: float = product_price_info["productPrice"]["current"]["value"]
    

    return name, price

