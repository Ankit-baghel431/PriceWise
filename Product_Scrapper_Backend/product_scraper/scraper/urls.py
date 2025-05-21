from django.urls import path
from .views import product_search

urlpatterns = [
    path('api/search/', product_search, name='product_search'),
]
