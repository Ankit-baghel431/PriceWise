import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

import time


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "DNT": "1",  # Do Not Track request
    "Connection": "keep-alive",
}


def scrape_amazon(search_query):
    base_url = "https://www.amazon.in/s?k="
    search_url = base_url + search_query.replace(" ", "+")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Amazon: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
        title_element = item.find("h2")
        price_element = item.find("span", {"class": "a-price-whole"})
        link_element = item.find("a", {"class": "a-link-normal"})
        img_element = item.find("img", {"class": "s-image"})

        if title_element and link_element:
            title = title_element.text.strip()
            price = price_element.text.strip() if price_element else "N/A"
            img = img_element["src"] if img_element else "N/A"
            link = "https://www.amazon.in" + link_element["href"]

            products.append(
                {
                    "title": title,
                    "price": price,
                    "image": img,
                    "seller": "Amazon",
                    "link": link
                }
            )

    return products



