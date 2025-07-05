from django.shortcuts import render
from . models import Sale


# Create your views here.


def sales_home(request):
    """
    Render the sales home page.
    """
    sales_list = Sale.objects.all()
    return render(request, 'sales/sales.html', {'sales_list': sales_list})