from django.shortcuts import render
from sales.models import Sale
from django.db.models import Sum
import random

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