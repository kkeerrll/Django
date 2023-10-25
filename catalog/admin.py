from django.contrib import admin

from catalog.models import Product, Category, Blog, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'text')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)


@admin.register(Blog)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'number', 'name', 'is_active']
    list_filter = ['product', 'is_active']
