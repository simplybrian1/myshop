# product/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),  # Product list page
    path('products/<int:id>/', views.product_detail, name='product_detail'),  # Product detail page
    # other product-related URLs...
]
