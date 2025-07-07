from django.urls import path
from . views import sales_home, add_sale, delete_sale

urlpatterns = [
    path('', sales_home, name='sales_home'),
    path('add_sale/', add_sale, name='add_sale'),
    path('delete/', delete_sale, name='delete_sale'),
]