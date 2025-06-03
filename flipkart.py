import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_flipkart_with_zenrows(search_query, api_key):
    search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '%20')}"

    params = {
        "apikey": api_key,
        "url": search_url,
        "js_render": "true",
        "premium_proxy": "true"
    }

    response = requests.get("https://api.zenrows.com/v1/", params=params)

    if response.status_code != 200:
        print("Request failed:", response.status_code, response.text)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("div", class_="_75nlfW"):
        try:
            link_tag = item.find("a", class_="CGtC98")
            name_tag = item.find("div", class_="KzDlHZ")
            price_tag = item.find("div", class_="Nx9bqj _4b5DiR")
            image_tag = item.find("img", class_="DByuf4")

            if link_tag and name_tag and price_tag and image_tag:
                product = {
                    "title": name_tag.text.strip(),
                    "price": price_tag.text.strip(),
                    "image": image_tag.get("src", "N/A"),
                    "seller": "Flipkart",
                    "link": "https://www.flipkart.com" + link_tag["href"]
                }
                products.append(product)
        except Exception as e:
            print("Error parsing a product:", e)
            continue

    return products

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    query = "laptop"
    results = scrape_flipkart_with_zenrows(query, api_key)

    print(json.dumps(results, indent=4))

    if results:
        with open("flipkart_products_zenrows.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'flipkart_products_zenrows.json'.")
    else:
        print("No products found or Flipkart blocked the request.")
