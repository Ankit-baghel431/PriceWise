import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json


async def scrape_myntra(search_query):
    search_url = (
        f"https://www.myntra.com/watches?rawQuery={search_query.replace(' ', '%20')}"
    )
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
        )
        page = await context.new_page()

        # Set extra HTTP headers
        await page.set_extra_http_headers(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
            }
        )

        # Navigate to the search page
        await page.goto(search_url, timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_selector("li.product-base", timeout=15000)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # Extract product data
        for item in soup.find_all("li", class_="product-base"):
            link_tag = item.find("a", href=True)
            link = "https://www.myntra.com" + link_tag["href"] if link_tag else None

            brand = item.find("h3", class_="product-brand")
            product_name = item.find("h4", class_="product-product")
            title = (
                f"{brand.text.strip()} - {product_name.text.strip()}"
                if brand and product_name
                else None
            )

            price_tag = item.find("span", class_="product-discountedPrice")
            price = price_tag.text.strip() if price_tag else None

            image_tag = item.find("img", class_="img-responsive")
            image = image_tag["src"] if image_tag else None

            if all([link, title, price, image]):
                products.append(
                    {
                        "title": title,
                        "price": price,
                        "image": image,
                        "seller": "Myntra",
                        "link": link,
                    }
                )

        await browser.close()
    return products


# Example execution
if __name__ == "__main__":
    query = "trolley bag"
    results = asyncio.run(scrape_myntra(query))
    print(json.dumps(results, indent=4))

    if results:
        with open("myntra_products_playwright.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'myntra_products_playwright.json'.")
    else:
        print("No products found or Myntra blocked the request.")
