import requests
from bs4 import BeautifulSoup

def scrape_myntra(search_query):
    base_url = "https://www.myntra.com/"
    search_url = base_url + search_query.replace(" ", "-")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(search_url, headers=headers, timeout=10)
    with open("myntra.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print(response.status_code)
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Myntra: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    # with open("myntra.html", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())
    # print(soup.prettify())
    products = []
    rts = soup.find("div", class_="search-searchProductsContainer row-base")
    print(rts)
    for item in soup.find_all("li", class_="product-base"):
        print(item)
        try:
            brand = item.find("h3", class_="product-brand").text.strip()
            title = item.find("h4", class_="product-product").text.strip()
            image_tag = item.find("img", class_="img-responsive")
            rating = item.find("div", class_="product-ratingsContainer")
            rating_value = rating.find("span").text.strip() if rating else None
            reviews_tag = item.find("div", class_="product-ratingsCount")
            reviews = reviews_tag.get_text(strip=True).replace("|", "") if reviews_tag else None

            discounted_price = item.find("span", class_="product-discountedPrice").text.strip()
            original_price = item.find("span", class_="product-strike").text.strip() if item.find("span", class_="product-strike") else None
            discount = item.find("span", class_="product-discountPercentage").text.strip() if item.find("span", class_="product-discountPercentage") else None

            product_link = base_url + item.find("a")["href"]
            image_url = image_tag["src"] if image_tag else None
            size = item.find("span", class_="product-sizeInventoryPresent")
            size_info = size.text.strip() if size else None

            products.append({
                "brand": brand,
                "title": title,
                "price": discounted_price,
                "original_price": original_price,
                "discount": discount,
                "rating": rating_value,
                "reviews": reviews,
                "size": size_info,
                "image": image_url,
                "link": product_link,
                "seller": "Myntra"
            })
        except Exception as err:
            print(f"Error parsing a product: {err}")

    return products

if __name__ == "__main__":
    products = scrape_myntra("bag")
    print(products)