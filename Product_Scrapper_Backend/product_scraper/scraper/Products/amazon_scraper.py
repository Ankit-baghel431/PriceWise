import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_amazon(search_query):
    search_url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 ...")
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

            if title_element and link_element:
                title = title_element.text.strip()
                link = "https://www.amazon.in" + link_element["href"]
                img = img_element["src"] if img_element else "N/A"
                price = price_element.text.strip().replace(",", "") if price_element else "N/A"
                mrp = mrp_element.text.strip().replace("₹", "").replace(",", "") if mrp_element else "N/A"

                discount_percentage = "N/A"
                if price != "N/A" and mrp != "N/A":
                    try:
                        discount_percentage = f"{round(((float(mrp) - float(price)) / float(mrp)) * 100)}% off"
                    except ValueError:
                        pass

                products.append({
                    "title": title,
                    "price": f"₹{price}" if price != "N/A" else "N/A",
                    "mrp": f"₹{mrp}" if mrp != "N/A" else "N/A",
                    "discount_percentage": discount_percentage,
                    "image": img,
                    "seller": "Amazon",
                    "link": link,
                })

        await browser.close()
    return products
