from django.contrib import admin
from . models import Product

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','stock','cost_price','selling_price','created_at')
    list_filter = ('name','category','stock','selling_price', 'cost_price','created_at')
    search_fields = ('name','category')
# admin.site.register(Product)
