from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from sales.models import Sale
from inventory.models import Product
from django.db.models import Sum
import random
from django.db.models.functions import TruncDate
import xlwt

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
    return render(request, 'reports/summary.html', {'context':context, 'v':v})


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

def export_filtered_products(request):

    category = request.GET.get('category', None)
    name = request.GET.get('name', None)
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)

    

    products = Product.objects.all()
    if category:
        products = Product.objects.filter(category=category)
        f_name = 'category'+ category + '.xls'



    if name:
        products = products.filter(name__icontains=name)
        f_name = 'name' + name + '.xls'

    if from_date and to_date:
        products = products.filter(created_at__range=[from_date, to_date])
        f_name = 'date_' + from_date + '_to_' + to_date + '.xls'

    

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{f_name}"'
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Filtered Products')
    columns = ['ID', 'Name', 'Category', 'Cost Price', 'Selling Price' , 'Created At']
    for col_num, col_title in enumerate(columns):
        worksheet.write(0, col_num, col_title)
    # Write product data
    # products = Product.objects.all()
    for row_num, product in enumerate(products, start=1):
        worksheet.write(row_num, 0, product.id)
        worksheet.write(row_num, 1, product.name)
        worksheet.write(row_num, 2, product.category)
        worksheet.write(row_num, 3, product.cost_price)
        worksheet.write(row_num, 4, product.selling_price)
        worksheet.write(row_num, 5, product.created_at.strftime('%Y-%m-%d %H:%M:%S'))
    workbook.save(response)
    return response