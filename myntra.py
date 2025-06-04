import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_myntra_with_zenrows(search_query, api_key):
    search_url = f"https://www.myntra.com/watches?rawQuery={search_query.replace(' ', '%20')}"

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

    for item in soup.find_all("li", class_="product-base"):
        try:
            link_tag = item.find("a", href=True)
            link = "https://www.myntra.com" + link_tag["href"] if link_tag else None

            brand = item.find("h3", class_="product-brand")
            product_name = item.find("h4", class_="product-product")
            title = f"{brand.text.strip()} - {product_name.text.strip()}" if brand and product_name else None

            price_tag = item.find("span", class_="product-discountedPrice")
            price = price_tag.text.strip() if price_tag else None

            image_tag = item.find("img", class_="img-responsive")
            image = image_tag.get("src") if image_tag else None

            if all([link, title, price, image]):
                products.append({
                    "title": title,
                    "price": price,
                    "image": image,
                    "seller": "Myntra",
                    "link": link
                })
        except Exception as e:
            print("Error parsing product:", e)
            continue

    return products

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    query = "trolley bag"
    results = scrape_myntra_with_zenrows(query, api_key)

    print(json.dumps(results, indent=4))

    if results:
        with open("myntra_products_zenrows.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'myntra_products_zenrows.json'.")
    else:
        print("No products found or Myntra blocked the request.")
