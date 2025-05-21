import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

async def scrape_amazon(search_query):
    search_url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        await page.goto(search_url, timeout=60000)
        await page.wait_for_selector("div[data-component-type='s-search-result']")

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        for item in soup.find_all("div", {"data-component-type": "s-search-result"}):
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
                    except ValueError:
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

        await browser.close()
    return products

# Run the async function
if __name__ == "__main__":
    query = "laptop"
    results = asyncio.run(scrape_amazon(query))
    print(json.dumps(results, indent=4))

    if results:
        with open("amazon_products_playwright.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'amazon_products_playwright.json'.")
    else:
        print("No products found or Amazon blocked the request.")
