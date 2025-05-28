import re
import asyncio
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .Products.amazon import search_amazon
from .Products.flipkart import search_flipkart
from .Products.scrape_ajio import scrape_ajio
from .Products.scrape_myntra import scrape_myntra

def run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(coro)

def home(request):
    query = request.GET.get('query')
    amazon_results, flipkart_results = [], []
    ajio_results, myntra_results = [], []

    if query:
        amazon_results = search_amazon(query)
        flipkart_results = search_flipkart(query)
        try:
            ajio_results = run_async(scrape_ajio(query))
        except Exception as e:
            print("Ajio error:", e)
        try:
            myntra_results = run_async(scrape_myntra(query))
        except Exception as e:
            print("Myntra error:", e)

    return render(request, 'scraper/index.html', {
        'query': query,
        'amazon_results': amazon_results,
        'flipkart_results': flipkart_results,
        'ajio_results': ajio_results,
        'myntra_results': myntra_results,
    })

@api_view(['GET'])
def product_search(request):
    query = request.GET.get('query', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if not query:
        return Response({"error": "No query provided"}, status=400)

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
        ajio_results = run_async(scrape_ajio(query))
    except Exception as e:
        print("Ajio error:", e)
        ajio_results = []

    try:
        myntra_results = run_async(scrape_myntra(query))
    except Exception as e:
        print("Myntra error:", e)
        myntra_results = []

    results = amazon_results + flipkart_results + ajio_results + myntra_results

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
    sorted_results = sorted(filtered_results, key=lambda p: (p['price'], -p['rating']))

    return Response({"results": sorted_results})
