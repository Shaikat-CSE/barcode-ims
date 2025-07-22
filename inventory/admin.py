# MongoEngine models are not compatible with Django admin
# This file is kept for reference but the admin registrations are removed

from django.contrib import admin
# from .models import Category, Product, ProductScan

# MongoEngine models cannot be registered with Django admin
# If you need admin functionality, consider using django-mongoengine or a custom admin interface

"""
# Original Django admin registrations (for reference)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'barcode', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'barcode', 'description')

@admin.register(ProductScan)
class ProductScanAdmin(admin.ModelAdmin):
    list_display = ('product', 'scanned_at')
    list_filter = ('scanned_at',)
    date_hierarchy = 'scanned_at'
"""
