import requests
from bs4 import BeautifulSoup
import os
import re
from dotenv import load_dotenv

load_dotenv()

def scrape_amazon(query):
    api_key = os.getenv("API_KEY")
    url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"

    params = {
        "apikey": api_key,
        "url": url,
        "js_render": "true",
        "premium_proxy": "true"
    }

    response = requests.get("https://api.zenrows.com/v1/", params=params)

    if response.status_code != 200:
        print("Amazon request failed:", response.status_code, response.text)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
        try:
            title_tag = item.find("h2")
            link_tag = item.find("a", {"class": "a-link-normal"})
            img_tag = item.find("img", {"class": "s-image"})
            price_tag = item.find("span", {"class": "a-price-whole"})
            rating_tag = item.find("span", {"class": "a-icon-alt"})

            if title_tag and link_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.amazon.in" + link_tag["href"]
                image = img_tag["src"] if img_tag else None
                price_text = price_tag.get_text(strip=True).replace(",", "") if price_tag else None
                price = float(price_text) if price_text and price_text.isdigit() else None
                rating_match = re.search(r"([\d.]+)", rating_tag.get_text()) if rating_tag else None
                rating = float(rating_match.group(1)) if rating_match else 0.0

                if title and price is not None:
                    products.append({
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "image": image,
                        "link": link,
                        "seller": "Amazon"
                    })
        except Exception as e:
            print("Amazon parse error:", e)
            continue

    return products
