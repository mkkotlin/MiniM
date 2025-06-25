from django.contrib import admin
from . models import Product, Sale

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','stock','cost_price','selling_price','created_at')
    list_filter = ('name','category','stock','selling_price', 'cost_price','created_at')
    search_fields = ('name','category')
# admin.site.register(Product)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','sale_price', 'date')
    list_filter = ('product','quantity','product__category', 'date')
    search_fields = ('product__name',)
# admin.site.register(Sale)