from django.urls import path
from .views import search_products

urlpatterns = [
    path("api/search/", search_products, name="search_products"),
]
