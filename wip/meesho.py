import requests
from bs4 import BeautifulSoup

def scrape_meesho(search_query):
    base_url = "https://www.meesho.com/search?q="
    search_url = base_url + search_query.replace(" ", "%20")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    print(response.status_code)
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Meesho: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    products = []

    for card in soup.find_all("div", class_="sc-dkrFOg"):
        try:
            link_tag = card.find("a")
            title_tag = card.find("p", class_="NewProductCardstyled__StyledDesktopProductTitle-sc-6y2tys-5")
            price_tag = card.find("h5")
            original_price_tag = card.find("p", class_="sc-eDvSVe drXXNP")
            discount_tag = card.find("span", class_="NewProductCardstyled__StyledDesktopSubtitle-sc-6y2tys-6")
            image_tag = card.find("img")

            rating_tag = card.find("span", class_="sc-eDvSVe laVOtN")
            review_tag = card.find("span", class_="NewProductCardstyled__RatingCount-sc-6y2tys-22")
            delivery_tag = card.find("span", string="Free Delivery")

            if link_tag and title_tag and price_tag and image_tag:
                product = {
                    "title": title_tag.text.strip(),
                    "price": price_tag.text.strip(),
                    "original_price": original_price_tag.text.strip() if original_price_tag else None,
                    "discount": discount_tag.text.strip() if discount_tag else None,
                    "rating": rating_tag.text.strip() if rating_tag else None,
                    "reviews": review_tag.text.strip() if review_tag else None,
                    "delivery": delivery_tag.text.strip() if delivery_tag else None,
                    "image": image_tag["src"],
                    "seller": "Meesho",
                    "link": "https://www.meesho.com" + link_tag["href"]
                }
                products.append(product)
        except Exception as err:
            print(f"Error parsing a product: {err}")

    return products


if __name__ == "__main__":

    products = scrape_meesho("bag")

    print(products)
