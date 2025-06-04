from playwright.async_api import async_playwright

async def scrape_ajio(query):
    products = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(f"https://www.ajio.com/search/?text={query}", wait_until="networkidle")

            items = await page.query_selector_all('.rilrtl-products-list .item')

            for item in items[:10]:
                title = await item.query_selector_eval('.nameCls', 'el => el.textContent', strict=False) or ""
                price = await item.query_selector_eval('.price .orginal-price', 'el => el.textContent', strict=False) or ""
                image = await item.query_selector_eval('img', 'el => el.src', strict=False) or ""
                link = await item.query_selector_eval('a', 'el => el.href', strict=False) or ""

                products.append({
                    "title": title.strip(),
                    "price": price.strip(),
                    "image": image.strip(),
                    "link": link.strip(),
                    "source": "Ajio",
                })

        except Exception as e:
            print(f"Ajio scraping failed: {e}")
        finally:
            await browser.close()

    return products
