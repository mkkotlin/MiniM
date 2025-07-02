from django.http import JsonResponse
from django.shortcuts import render, redirect
from . models import Product
from django.template.loader import render_to_string

# Create your views here.

def inventory_list(request):
    """Render the inventory list page.
    Args:
        request: The HTTP request object.
    Returns:
        HttpResponse: Rendered HTML page with the list of products."""
    products = Product.objects.all().order_by('-created_at')
    return render(request,'inventory/inventory.html', {'products':products})
    

def add_product(request):
    """Add a new product to the inventory.
    Args:
        request: The HTTP request object.
    Returns:
        JsonResponse: A JSON response indicating success or failure."""
    if request.method == 'POST':
        try:
            name = request.POST['name']
            category = request.POST['category']
            stock = int(request.POST['stock'])
            cost_price = float(request.POST['cost_price'])
            selling_price = float(request.POST['selling_price'])

            if selling_price < cost_price:
                return JsonResponse({'status':'error','message':'sell price cant be smaller than cost price'}, status=400)
            if selling_price <=0 or cost_price <= 0:
                return JsonResponse({'status':'error','message':'price must be more than 0'}, status=400) 
            
            product = Product.objects.create(name=name, category=category, stock=stock, cost_price=cost_price, selling_price=selling_price)
            rendred_row = render_to_string('inventory/product_row.html',{'p':product})
            return JsonResponse({'success':f'added to inventory with p_id: {product.id}', 'row_html':rendred_row})
        except (ValueError, TypeError)as e:
            return JsonResponse({'status':'error', 'message':f'invalid input: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'status':'error', 'message':f'Something went wrong: {e}'}, status=500)
    return JsonResponse({'status':'error', 'message':'Invalid request method'},status=405)

def delete_product(request, id):
    """"Delete a product by its ID.
    Args:
        request: The HTTP request object.
        id (int): The ID of the product to delete.
    """
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return JsonResponse({'status':'success', 'message':'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'status':'error', 'message':'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status':'error', 'message':f'Something went wrong: {e}'}, status=500)
    
def update_product(request, id):
    pass