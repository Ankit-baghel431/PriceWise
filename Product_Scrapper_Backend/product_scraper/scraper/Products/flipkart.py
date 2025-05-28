import asyncio
from .flipkart_scraper import scrape_flipkart

def search_flipkart(query):
    return asyncio.run(scrape_flipkart(query))
