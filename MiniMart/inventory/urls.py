from django.urls import path
from . views import inventory_list, add_product, delete_product

urlpatterns = [
    path('', inventory_list, name='inventory_list'),
    path('add/', add_product, name='add_product'),
    path('delete/<int:id>/', delete_product, name='delete_product'),
]