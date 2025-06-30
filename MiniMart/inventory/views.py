from django.shortcuts import render
from . models import Product

# Create your views here.

def inventory_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request,'inventory/inventory.html', {'products':products})
    

def add_product(request):
    pass

def delete_product(request, id):
    pass