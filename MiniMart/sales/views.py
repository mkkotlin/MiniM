from django.shortcuts import render
from . models import Sale
from inventory.models import Product
from django.http import JsonResponse
from django.template.loader import render_to_string


# Create your views here.


def sales_home(request):
    """
    Render the sales home page.
    """
    sales_list = Sale.objects.all().order_by('-date')
    product = Product.objects.all()
    return render(request, 'sales/sales.html', {'sales_list': sales_list,'products':product})


def add_sale(request):
    """
    Handle the addition of a new sale.
    This function processes POST requests to add a sale and updates the product stock accordingly.
    Args:
        request (HttpRequest): The HTTP request object containing the sale data.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        sale_price = float(request.POST.get('sale_price'))

        try:
            product = Product.objects.get(id=product_id)
            if quantity > product.stock:
                return JsonResponse({'status':'error','message':f'Not enough stock {product.stock}'}, status=400)
            
            sales = Sale.objects.create(product = product, quantity = quantity, sale_price = sale_price)
            product.stock -= quantity
            product.save()
            rendered_row = render_to_string('sales/sale_row.html', {'s': sales})
            return JsonResponse({'status':'success','message':'sale added & updated','row':rendered_row}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'status':'error','message':'Product not found'}, status=404)
    return JsonResponse({'status':'error', 'message':'invalid request'}, status=405)

        # Sale.objects.create(product = product, quantity = quantity, sale_price = sale_price)


def delete_sale(request, id):
    """ Handle the deletion of a sale by its ID.
    This function processes DELETE requests to remove a sale and updates the product stock accordingly.
    Args:   
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the sale to be deleted.
    Returns:
        JsonResponse: A JSON response indicating the success or failure of the deletion."""
    try:
        sale = Sale.objects.get(id=id)
        sale.delete()
        return JsonResponse({'status':'success', 'message':f'{id} Sale deleted'})
    except Sale.DoesNotExist:
        return JsonResponse({'status':'error','message':'Product not found'}, status=404)