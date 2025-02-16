# admin.py
from django.contrib import admin
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
