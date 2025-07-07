from django.urls import path
from . views import sales_home, add_sale

urlpatterns = [
    path('', sales_home, name='sales_home'),
    path('add_sale/', add_sale, name='add_sale'),
]