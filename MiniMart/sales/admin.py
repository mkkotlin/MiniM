from django.contrib import admin
from . models import Sale

# Register your models here.
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','sale_price', 'date')
    list_filter = ('product','quantity','product__category', 'date')
    search_fields = ('product__name',)
# admin.site.register(Sale)