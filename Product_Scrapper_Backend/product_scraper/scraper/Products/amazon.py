# scraper/Products/amazon.py
import asyncio
from .amazon_scraper import scrape_amazon

def search_amazon(query):
    return asyncio.run(scrape_amazon(query))
