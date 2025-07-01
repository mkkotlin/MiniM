from django.http import JsonResponse
from django.shortcuts import render, redirect
from . models import Product

# Create your views here.

def inventory_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request,'inventory/inventory.html', {'products':products})
    

def add_product(request):
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
            return JsonResponse({'success':f'added to inventory with p_id: {product.id}'})
        except (ValueError, TypeError)as e:
            return JsonResponse({'status':'error', 'message':f'invalid input: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'status':'error', 'message':f'Something went wrong: {e}'}, status=500)
    return JsonResponse({'status':'error', 'message':'Invalid request method'},status=405)

def delete_product(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return JsonResponse({'status':'success', 'message':'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'status':'error', 'message':'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status':'error', 'message':f'Something went wrong: {e}'}, status=500)