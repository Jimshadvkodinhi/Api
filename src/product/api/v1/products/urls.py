from django.urls import path
from main.views import *
from api.v1.products.views import *


urlpatterns = [
    path('categories/', list_categories, name='category-list'),
    path('categories/<int:pk>/', get_category, name='category-single'),
    path('categories/create/', create_category, name='category-create'),
    path('products/', list_products, name='product-list'),
    path('products/<int:pk>/', get_product, name='product-single'),
    path('products/create/', create_product, name='product-create'),
]