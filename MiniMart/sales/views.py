from django.shortcuts import render
from . models import Sale
from inventory.models import Product
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import json
import time
import csv
import xlwt


# Create your views here.


def sales_home(request):
    """
    Render the sales home page.
    """
    sales_list = Sale.objects.all().order_by('-date')
    product = Product.objects.all()
    return render(request, 'sales/sales.html', {'sales_list': sales_list,'products':product, 'current_time': int(time.time()*1000)})


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


def update_sale(request,id):
    """
    Handle the update of an existing sale.
    This function processes POST requests to update a sale's details and adjusts the product stock accordingly.
    Args:
        request (HttpRequest): The HTTP request object containing the sale data.
        id (int): The ID of the sale to be updated.
    Returns:
        JsonResponse: A JSON response indicating the success or failure of the update.
    """
    if request.method == 'POST':
        id = request.POST.get('id')
        quantity = int(request.POST.get('quantity'))
        sale_price = float(request.POST.get('price'))
        print(sale_price, quantity, id)
        try:
            sale = Sale.objects.get(id=id)
            product = Product.objects.get(id=sale.product.id)
            original_quantity = sale.quantity
            original_product = sale.product
            original_sale_price = sale.sale_price
            if quantity > product.stock:
                return JsonResponse({'status':'error','message':f'Not enough stock {product.stock}'}, status=400)
            sale.product = product
            sale.quantity = quantity
            sale.sale_price = sale_price
            sale.save()
            product.stock -= quantity
            product.save()
            return JsonResponse({'status':'success','message':'Sale updated successfully'}, status=200)
        except Sale.DoesNotExist:
            return JsonResponse({'status':'error','message':'Sale not found'}, status=404)
        except Product.DoesNotExist:
            return JsonResponse({'status':'error','message':'Product not found'}, status=404)
        except ValueError:
            return JsonResponse({'status':'error','message':'Invalid input data'}, status=400)
        except:
            return JsonResponse({'status':'error','message':'An unexpected error occurred'}, status=500)


def add_multiple_sales(request):
    """
    Handle the addition of multiple sales.
    This function processes POST requests to add multiple sales and updates the product stock accordingly.
    Args:
        request (HttpRequest): The HTTP request object containing the sale data.
    """
    if request.method == 'POST':
        sales_data = json.loads(request.body)
        print(sales_data)
        rendered_rows = []
        for sale_data in sales_data:
            product_id = sale_data.get('product')
            quantity = int(sale_data.get('quantity',0))
            sale_price = float(sale_data.get('sale_price',0))
            
            try:
                product = Product.objects.get(id=product_id)
                if quantity > product.stock:
                    return JsonResponse({'status':'error','message':f'Not enough stock {product.stock}'}, status=400)

                sale = Sale.objects.create(product=product, quantity=quantity, sale_price=sale_price)
                product.stock -= quantity
                product.save()
                
                rendered_row = render_to_string('sales/sale_row.html', {'s': sale})
                rendered_rows.append(rendered_row)
            except Product.DoesNotExist:
                return JsonResponse({'status':'error','message':'Product not found'}, status=404)
            except ValueError:
                return JsonResponse({'status':'error','message':'Invalid input data'}, status=400)
        return JsonResponse({'status':'success','message':'Multiple sales added successfully', 'rows': rendered_rows}, status=200)
    return JsonResponse({'status':'error', 'message':'invalid request'}, status=405)


def export_sales(request, file_format):
    if file_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Product', 'Quantity', 'Sale Price', 'Date'])
        sales = Sale.objects.all()
        for sale in sales:
            writer.writerow([sale.id, sale.product.name, sale.quantity, sale.sale_price, sale.date])
        return response
    # This function exports all sales data to a CSV file.
    # It sets the content type to 'text/csv' and writes the header row followed by
    elif file_format == 'xls':
        return export_xls(request)          
    
    elif file_format == 'json':
        return export_json(request)

def export_xls(request):
    # Create a new Excel workbook and sheet
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Sales')

    # Define column headers
    columns = ['Product', 'Quantity', 'Sale Price', 'Date']

    # Write column headers in bold
    bold_style = xlwt.XFStyle()
    bold_font = xlwt.Font()
    bold_font.bold = True
    bold_style.font = bold_font

    for col_num, column_title in enumerate(columns):
        sheet.write(0, col_num, column_title, bold_style)

    # Write data rows
    for row_num, sale in enumerate(Sale.objects.all().order_by('-date'), start=1):
        sheet.write(row_num, 0, sale.product.name)
        sheet.write(row_num, 1, sale.quantity)
        sheet.write(row_num, 2, float(sale.sale_price))
        sheet.write(row_num, 3, sale.date.strftime("%Y-%m-%d %H:%M"))

    # Prepare response
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales.xls"'
    workbook.save(response)
    return response

def export_json(request):
    sales = Sale.objects.all()
    data = []
    for sale in sales:
        data.append({
            'id': sale.id,
            'product': sale.product.name,
            'quantity': sale.quantity,
            'sale_price': str(sale.sale_price),
            'date': sale.date.strftime("%Y-%m-%d %H:%M")
        })
        response = HttpResponse(json.dumps(data, indent=4), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="sales.json"'
    return response