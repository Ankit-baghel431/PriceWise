from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .Products.amazon import search_amazon
from .Products.flipkart import search_flipkart
from .Products.scrape_myntra import scrape_myntra

import asyncio
import re

def run_async(coro):
    try:
        # Try to run normally (works if no event loop running)
        return asyncio.run(coro)
    except RuntimeError:
        # If event loop already running, create a new loop and run coroutine there
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

def home(request):
    query = request.GET.get('query')
    amazon_results, flipkart_results, myntra_results = [], [], []

    if query:
        amazon_results = search_amazon(query)
        flipkart_results = search_flipkart(query)
        try:
            myntra_results = run_async(scrape_myntra(query))
        except Exception as e:
            print("Myntra error:", e)

    return render(request, 'scraper/index.html', {
        'query': query,
        'amazon_results': amazon_results,
        'flipkart_results': flipkart_results,
        'myntra_results': myntra_results,
    })

@api_view(['GET'])
def product_search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return Response({"error": "No query provided"}, status=400)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    try:
        min_price = float(min_price) if min_price else None
    except ValueError:
        min_price = None

    try:
        max_price = float(max_price) if max_price else None
    except ValueError:
        max_price = None

    amazon_results = search_amazon(query)
    flipkart_results = search_flipkart(query)
    try:
        myntra_results = run_async(scrape_myntra(query))
    except Exception as e:
        print("Myntra error:", e)
        myntra_results = []

    results = amazon_results + flipkart_results + myntra_results

    def clean_product(product):
        try:
            price_val = float(re.sub(r'[^\d.]', '', str(product.get('price', '0'))))
            product['price'] = price_val
        except:
            product['price'] = float('inf')

        try:
            product['rating'] = float(product.get('rating', 0))
        except:
            product['rating'] = 0.0

        return product

    cleaned_results = [clean_product(p) for p in results]

    def in_price_range(product):
        if min_price is not None and product['price'] < min_price:
            return False
        if max_price is not None and product['price'] > max_price:
            return False
        return True

    filtered_results = list(filter(in_price_range, cleaned_results))

    # Sort by price ascending, rating descending
    sorted_results = sorted(filtered_results, key=lambda p: (p['price'], -p['rating']))

    return Response({"results": sorted_results})
    