from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.product_search, name='product_search'),
    path('', views.home, name='home'),
]
