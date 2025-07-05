from django.urls import path
from . views import sales_home

urlpatterns = [
    path('', sales_home, name='sales_home'),
]