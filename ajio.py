import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json


async def scrape_ajio(search_query):
    search_url = f"https://www.ajio.com/search/?text={search_query.replace(' ', '%20')}"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox",
            ]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
        )

        # Remove navigator.webdriver flag
        page = await context.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            });
        """)

        await page.set_extra_http_headers(
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/",
            }
        )
        await page.goto(search_url, timeout=60000, wait_until="networkidle")

        try:
            await page.wait_for_selector("div.item", timeout=20000)
        except:
            # Take a screenshot for debugging
            await page.screenshot(path="ajio_error.png")
            print("⚠️ Could not find selector — saved screenshot to 'ajio_error.png'")

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        for item in soup.find_all("div", class_="rilrtl-products-list__item"):
            try:
                link_tag = item.find("a", class_="rilrtl-products-list__link")
                img_tag = item.find("img", class_="rilrtl-lazy-img")
                brand_tag = item.find("div", class_="brand")
                name_tag = item.find("div", class_="nameCls")
                price_tag = item.find("span", class_="price")
                original_price_tag = item.find("span", class_="orginal-price")
                discount_tag = item.find("span", class_="discount")
                offer_price_tag = item.find("span", class_="offer-pricess-new")

                product = {
                    "title": name_tag.text.strip() if name_tag else None,
                    "brand": brand_tag.text.strip() if brand_tag else None,
                    "price": price_tag.text.strip() if price_tag else None,
                    "original_price": original_price_tag.text.strip() if original_price_tag else None,
                    "discount": discount_tag.text.strip() if discount_tag else None,
                    "offer_price": offer_price_tag.text.strip() if offer_price_tag else None,
                    "image": img_tag["src"] if img_tag else None,
                    "link": "https://www.ajio.com" + link_tag["href"] if link_tag else None
                }

                products.append(product)
            except Exception as e:
                print("❌ Error parsing product:", e)

        await browser.close()
    return products


# Run it
if __name__ == "__main__":
    query = "shirt"
    results = asyncio.run(scrape_ajio(query))
    print(json.dumps(results, indent=4))

    if results:
        with open("ajio_products.json", "w") as f:
            json.dump(results, f, indent=4)
        print("✅ Products saved to 'ajio_products.json'.")
    else:
        print("❌ No products found or AJIO blocked the request.")
