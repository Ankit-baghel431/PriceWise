import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

import time




def scrape_flipkart(search_query):
    base_url = "https://www.flipkart.com/search?q="
    search_url = base_url + search_query.replace(" ", "%20")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Flipkart: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("div", class_="_75nlfW"):
        link_tag = item.find("a", class_="CGtC98")
        name_tag = item.find("div", class_="KzDlHZ")
        price_tag = item.find("div", class_="Nx9bqj _4b5DiR")
        image_tag = item.find("img", class_="DByuf4")

        if link_tag and name_tag and price_tag and image_tag:
            product = {
                "title": name_tag.text.strip(),
                "price": price_tag.text.strip(),
                "image": image_tag["src"],
                "seller": "Flipkart",
                "link": "https://www.flipkart.com" + link_tag["href"],
            }
            products.append(product)

    return products

