from django.http import JsonResponse
from django.shortcuts import render
from sales.models import Sale
from inventory.models import Product
from django.db.models import Sum
import random
from django.db.models.functions import TruncDate

# Create your views here.


def sales_summary(request):
    total_sale = Sale.objects.count()
    total_quantity = Sale.objects.aggregate(total = Sum('quantity'))['total'] or 0
    total_revenue = Sale.objects.aggregate(total = Sum('sale_price'))['total'] or 0

    top_products= (Sale.objects.values('product__name').annotate(total_sold = Sum('quantity')).order_by('-total_sold')[:5])
    v = random.randint(1,10)
    context = {
        'total_sales':total_sale,
        'total_quantity':total_quantity,
        'total_revenue': total_revenue,
        'top_products': top_products,
        'v':v,
    }
    return render(request, 'reports/summary.html', {'context':context})


def advance_report(request):
    products = Product.objects.all()
    cat = Product.objects.values_list('category', flat=True).distinct()
    return render(request, 'reports/advance_report.html', {'products':products, 'cat':cat})


def get_product_category(request, cat):
    products = Product.objects.filter(category=cat)
    return JsonResponse({'products': list(products.values())})

def get_product_name(request, name):
    print(name)
    products = Product.objects.filter(name__icontains=name)
    return JsonResponse({'products': list(products.values())})

def get_product_date(request, from_date, to_date):
    print(from_date, to_date)
    # products = Product.objects.filter(created_at__range=[from_date, to_date])
    products = Product.objects.annotate(day = TruncDate('created_at')).filter(day__range=[from_date, to_date])
    return JsonResponse({'products': list(products.values())})

def get_product_all(request):
    products = Product.objects.all()
    return JsonResponse({'products': list(products.values())})