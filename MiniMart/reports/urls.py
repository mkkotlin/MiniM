from django.urls import path
from . views import sales_summary,  advance_report, get_product_category, get_product_name, get_product_date, get_product_all

urlpatterns = [
    path('summary/', sales_summary, name='sales_summary'),
    path('advance_report/', advance_report, name='advance_report'),
    path('get_product_category/<str:cat>/', get_product_category, name='get_product_category'),
    path('get_product_name/<str:name>/', get_product_name, name='get_product_name'),
    path('get_product_date/<str:from_date>/<str:to_date>/', get_product_date, name='get_product_date'),
    path('get_product_all/', get_product_all, name='get_product_all'),
]