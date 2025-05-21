import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json

async def scrape_flipkart(search_query):
    search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '%20')}"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        await page.goto(search_url, timeout=60000)
        await page.wait_for_selector("div._75nlfW", timeout=15000)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        for item in soup.find_all("div", class_="_75nlfW"):
            link_tag = item.find("a", class_="CGtC98")
            name_tag = item.find("div", class_="KzDlHZ")
            price_tag = item.find("div", class_="Nx9bqj _4b5DiR")
            image_tag = item.find("img", class_="DByuf4")

            if link_tag and name_tag and price_tag and image_tag:
                product = {
                    "title": name_tag.text.strip(),
                    "price": price_tag.text.strip(),
                    "image": image_tag["src"],
                    "seller": "Flipkart",
                    "link": "https://www.flipkart.com" + link_tag["href"],
                }
                products.append(product)

        await browser.close()
    return products

# Example execution
if __name__ == "__main__":
    query = "laptop"
    results = asyncio.run(scrape_flipkart(query))
    print(json.dumps(results, indent=4))

    if results:
        with open("flipkart_products_playwright.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'flipkart_products_playwright.json'.")
    else:
        print("No products found or Flipkart blocked the request.")
