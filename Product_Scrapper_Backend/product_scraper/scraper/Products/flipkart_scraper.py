import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_flipkart(search_query):
    search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '%20')}"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 ...")
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
