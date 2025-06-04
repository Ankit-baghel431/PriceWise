import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


async def scrape_amazon(search_query):
    search_url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/112.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()
        await page.goto(search_url, timeout=60000)
        await page.wait_for_selector("div[data-component-type='s-search-result']", timeout=15000)

        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        for item in soup.select("div[data-component-type='s-search-result']"):
            try:
                title_element = item.find("h2")
                link_element = item.find("a", {"class": "a-link-normal"})
                img_element = item.find("img", {"class": "s-image"})
                price_element = item.find("span", {"class": "a-price-whole"})
                mrp_element = item.select_one("span.a-price.a-text-price span.a-offscreen")

                if not title_element or not link_element:
                    continue

                title = title_element.get_text(strip=True)
                link = "https://www.amazon.in" + link_element["href"]
                img = img_element["src"] if img_element else "N/A"
                price = price_element.get_text(strip=True).replace(",", "") if price_element else "N/A"
                mrp = mrp_element.get_text(strip=True).replace("₹", "").replace(",", "") if mrp_element else "N/A"

                discount_percentage = "N/A"
                if price != "N/A" and mrp != "N/A":
                    try:
                        price_val = float(price)
                        mrp_val = float(mrp)
                        discount = round(((mrp_val - price_val) / mrp_val) * 100)
                        discount_percentage = f"{discount}% off"
                    except Exception:
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

            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        await browser.close()

    return products
