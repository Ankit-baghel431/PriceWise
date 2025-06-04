import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

def search_flipkart(query):
    api_key = os.getenv("API_KEY")
    url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"

    params = {
        "apikey": api_key,
        "url": url,
        "js_render": "true",
        "premium_proxy": "true"
    }

    response = requests.get("https://api.zenrows.com/v1/", params=params)

    if response.status_code != 200:
        print("Flipkart request failed:", response.status_code, response.text)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("div", class_="_75nlfW"):
        try:
            name_tag = item.find("div", class_="KzDlHZ")
            price_tag = item.find("div", class_="Nx9bqj _4b5DiR")
            image_tag = item.find("img", class_="DByuf4")
            link_tag = item.find("a", class_="CGtC98")

            if name_tag and price_tag and image_tag and link_tag:
                title = name_tag.text.strip()
                price_text = price_tag.text.strip().replace("₹", "").replace(",", "")
                price = float(price_text) if price_text.replace('.', '', 1).isdigit() else None
                image = image_tag["src"]
                link = "https://www.flipkart.com" + link_tag["href"]

                if title and price:
                    products.append({
                        "title": title,
                        "price": price,
                        "rating": 0.0,  # Rating not scraped here
                        "image": image,
                        "link": link,
                        "seller": "Flipkart"
                    })
        except Exception as e:
            print("Flipkart parse error:", e)
            continue

    return products
