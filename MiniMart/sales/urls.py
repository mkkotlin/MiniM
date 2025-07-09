from django.urls import path
from . views import sales_home, add_sale, delete_sale, update_sale

urlpatterns = [
    path('', sales_home, name='sales_home'),
    path('add_sale/', add_sale, name='add_sale'),
    path('delete/<int:id>/', delete_sale, name='delete_sale'),
    path('edit/<int:id>/', update_sale, name='update_sale'),
]