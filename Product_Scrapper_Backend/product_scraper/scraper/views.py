from rest_framework.decorators import api_view
from rest_framework.response import Response
import asyncio
import re
from collections import defaultdict

from .Products.amazon import search_amazon
from .Products.flipkart import search_flipkart
from .Products.scrape_myntra import scrape_myntra


from django.shortcuts import render

def home(request):
    return render(request, 'scraper/index.html')


def run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

@api_view(['GET'])
def product_search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return Response({"error": "No query provided"}, status=400)

    try:
        min_price = float(request.GET.get('min_price')) if request.GET.get('min_price') else None
    except ValueError:
        min_price = None

    try:
        max_price = float(request.GET.get('max_price')) if request.GET.get('max_price') else None
    except ValueError:
        max_price = None

    amazon_results, flipkart_results, myntra_results = [], [], []

    try:
        amazon_results = search_amazon(query)
        for p in amazon_results:
            p['source'] = 'Amazon'
    except Exception as e:
        print("Amazon error:", e)

    try:
        flipkart_results = search_flipkart(query)
        for p in flipkart_results:
            p['source'] = 'Flipkart'
    except Exception as e:
        print("Flipkart error:", e)

    try:
        myntra_results = run_async(scrape_myntra(query))
        for p in myntra_results:
            p['source'] = 'Myntra'
    except Exception as e:
        print("Myntra error:", e)

    all_results = amazon_results + flipkart_results + myntra_results

    def clean_product(p):
        try:
            p['price'] = float(re.sub(r'[^\d.]', '', str(p.get('price', '0'))))
        except:
            p['price'] = float('inf')

        try:
            p['rating'] = float(p.get('rating', 0))
        except:
            p['rating'] = 0.0

        return p

    cleaned_results = [clean_product(p) for p in all_results]

    def in_price_range(p):
        if min_price is not None and p['price'] < min_price:
            return False
        if max_price is not None and p['price'] > max_price:
            return False
        return True

    filtered = list(filter(in_price_range, cleaned_results))

    sorted_results = sorted(filtered, key=lambda p: (p['price'], -p['rating']))

    grouped = defaultdict(list)
    for product in sorted_results:
        grouped[product.get('source', 'Unknown')].append(product)

    grouped_results = dict(grouped)

    return Response({
        "query": query,
        "count": len(sorted_results),
        "results_by_source": grouped_results
    })