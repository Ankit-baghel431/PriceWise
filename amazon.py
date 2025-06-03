import requests
from bs4 import BeautifulSoup
import json
import os

from dotenv import load_dotenv

load_dotenv()

def scrape_amazon_with_zenrows(search_query, api_key):
    search_url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"

    params = {
        "apikey": api_key,
        "url": search_url,
        "js_render": "true",  # Enables JS rendering
        "premium_proxy": "true",  # Reduces risk of blocks
    }

    response = requests.get("https://api.zenrows.com/v1/", params=params)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
        try:
            title_element = item.find("h2")
            link_element = item.find("a", {"class": "a-link-normal"})
            img_element = item.find("img", {"class": "s-image"})
            price_element = item.find("span", {"class": "a-price-whole"})
            mrp_element = item.find("span", {"class": "a-offscreen"})
            star_rating_element = item.find("span", {"class": "a-icon-alt"})
            review_count_element = item.find("span", {"class": "a-size-base"})
            tag_element = item.find("span", {"class": "a-badge-text"})
            delivery_element = item.find("span", {"class": "a-color-base a-text-bold"})

            if title_element and link_element:
                title = title_element.text.strip()
                link = "https://www.amazon.in" + link_element["href"]
                img = img_element["src"] if img_element else "N/A"
                price = price_element.text.strip().replace(",", "") if price_element else "N/A"
                mrp = mrp_element.text.strip().replace("₹", "").replace(",", "") if mrp_element else "N/A"

                if price != "N/A" and mrp != "N/A":
                    try:
                        price_float = float(price)
                        mrp_float = float(mrp)
                        discount_percentage = f"{round(((mrp_float - price_float) / mrp_float) * 100)}% off"
                    except:
                        discount_percentage = "N/A"
                else:
                    discount_percentage = "N/A"

                star_rating = star_rating_element.text.strip() if star_rating_element else "N/A"
                review_count = review_count_element.text.strip() if review_count_element else "N/A"
                tag = tag_element.text.strip() if tag_element else "None"
                delivery = delivery_element.text.strip() if delivery_element else "N/A"

                products.append({
                    "title": title,
                    "price": f"₹{price}" if price != "N/A" else "N/A",
                    "mrp": f"₹{mrp}" if mrp != "N/A" else "N/A",
                    "discount_percentage": discount_percentage,
                    "image": img,
                    "seller": "Amazon",
                    "link": link,
                    "star_rating": star_rating,
                    "review_count": review_count,
                    "tag": tag,
                    "delivery": delivery,
                })
        except Exception as e:
            print("Error parsing a product:", e)
            continue

    return products

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    query = "laptop"

    results = scrape_amazon_with_zenrows(query, api_key)
    print(json.dumps(results, indent=4))

    if results:
        with open("amazon_products_zenrows.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'amazon_products_zenrows.json'.")
    else:
        print("No products found or request failed.")
