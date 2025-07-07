from django.shortcuts import render
from . models import Sale
from inventory.models import Product
from django.http import JsonResponse


# Create your views here.


def sales_home(request):
    """
    Render the sales home page.
    """
    sales_list = Sale.objects.all()
    product = Product.objects.all()
    return render(request, 'sales/sales.html', {'sales_list': sales_list,'products':product})


def add_sale(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        sale_price = float(request.POST.get('sale_price'))

        try:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                return JsonResponse({'status':'error','message':f'Not enough stock {product.stock}'}, status=400)
            
            Sale.objects.create(product = product, quantity = quantity, sale_price = sale_price)
            product.stock -= quantity
            product.save()
            return JsonResponse({'status':'success','message':'sale added & updated'}, status=200)
        except Product.DoNotExist:
            return JsonResponse({'status':'error','message':'Product not fount'}, status=404)
    return JsonResponse({'status':'error', 'message':'inavlid request'}, status=405)

        # Sale.objects.create(product = product, quantity = quantity, sale_price = sale_price)
        