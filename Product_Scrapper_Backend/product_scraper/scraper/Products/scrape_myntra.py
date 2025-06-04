import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

async def scrape_myntra(query):
    api_key = os.getenv("API_KEY")
    search_url = f"https://www.myntra.com/all?rawQuery={query.replace(' ', '%20')}"

    params = {
        "apikey": api_key,
        "url": search_url,
        "js_render": "true",
        "premium_proxy": "true"
    }

    response = requests.get("https://api.zenrows.com/v1/", params=params)

    if response.status_code != 200:
        print("Myntra request failed:", response.status_code, response.text)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("li", class_="product-base"):
        try:
            link_tag = item.find("a", href=True)
            brand = item.find("h3", class_="product-brand")
            product_name = item.find("h4", class_="product-product")
            price_tag = item.find("span", class_="product-discountedPrice")
            image_tag = item.find("img", class_="img-responsive")

            if link_tag and brand and product_name and price_tag and image_tag:
                title = f"{brand.text.strip()} - {product_name.text.strip()}"
                price_text = price_tag.text.strip().replace("₹", "").replace(",", "")
                price = float(price_text) if price_text.replace('.', '', 1).isdigit() else None
                image = image_tag.get("src", "N/A")
                link = "https://www.myntra.com" + link_tag["href"]

                if title and price:
                    products.append({
                        "title": title,
                        "price": price,
                        "rating": 0.0,  # Myntra doesn't show ratings
                        "image": image,
                        "link": link,
                        "seller": "Myntra"
                    })
        except Exception as e:
            print("Myntra parse error:", e)
            continue

    return products
