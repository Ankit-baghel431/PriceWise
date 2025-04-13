from rest_framework.decorators import api_view
from rest_framework.response import Response
from .Products.amazon import search_amazon
from .Products.flipkart import search_flipkart

@api_view(['GET'])
def product_search(request):
    query = request.GET.get('query', '')
    if not query:
        return Response({"error": "No query provided"}, status=400)
    
    amazon_results = search_amazon(query)
    flipkart_results = search_flipkart(query)

    results = {
        "amazon": amazon_results,
        "flipkart": flipkart_results
    }

    return Response(results)
