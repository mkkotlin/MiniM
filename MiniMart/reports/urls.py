from django.urls import path
from . views import sales_summary

urlpatterns = [
    path('summary/', sales_summary, name='sales_summary')
]