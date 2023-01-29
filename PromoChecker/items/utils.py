from typing import Dict, Tuple
import json

import requests
from bs4 import BeautifulSoup


def get_item_data(url: str, store: str) -> Tuple[str, float]:
    """parses an item's web page and extract relevant information

    Args:
        store (str): to point to which store should the data be extracted from

    Returns:
        name, price (Tuple): name of the product, its price
    """

    try:
        if store == "asos":
            return _data_extraction_asos(url=url)
        elif store == "zalando":
            return _data_extraction_zalando(url=url)
    except Exception:
        return ('not found', -404)


def _data_extraction(data_extraction_func):
    """Decorator function create function for data extraction from the different web stores

    Args:
        data_extraction_func (function): function for data extraction from a specific web store
    """
    
    def wrapper(*args, **kwargs):
        """wrapper function
        """
        
        headers: Dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "Accept-Languages": "en-GB, en-US, fr"
        }
        response: requests.Response = requests.get(kwargs['url'], headers=headers)
        page_parsed: BeautifulSoup = BeautifulSoup(response.text, "lxml")
        name_price: Tuple[str, float] = data_extraction_func(
            headers=headers,
            page_parsed=page_parsed
        )
        return name_price
    return wrapper
 

@_data_extraction
def _data_extraction_asos(**kwargs) -> Tuple[str, float]:
    """extracts item's data from the asos marketplace

    Args:
        url (str): item's web page url
        page_parsed (BeautifulSoup): item's web page parsed using Beautiful soup

    Returns:
        Tuple[str, str]: name and price of the item
    """
    
    product_data: str = json.loads(
        kwargs['page_parsed'].find('script', type='application/ld+json').string
    )
    item_name: str = product_data['name']
    price_endpoint: str = (
        f"https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={product_data['productID']}&store=FR&currency=EUR"
    )
    product_price_info: Dict = requests.get(
        price_endpoint, headers=kwargs['headers']).json()[0]
    item_price: float = product_price_info["productPrice"]["current"]["value"]
    
    return item_name, item_price

@_data_extraction
def _data_extraction_zalando(**kwargs) -> Tuple[str, float]:
    """extracts item's data from the asos marketplace

    Args:
        url (str): item's web page url
        page_parsed (BeautifulSoup): item's web page parsed using Beautiful soup

    Returns:
        Tuple[str, str]: name and price of the item
    """
    
    item_name: str = kwargs['page_parsed'].find(
        "meta", attrs={"property": "og:title"}
    )["content"]
    item_price: float = float(
        kwargs['page_parsed'].find(
            "meta", attrs={"name": "twitter:data1"}
        )["content"].replace(",", ".")[:5]
    )
    
    return item_name, item_price