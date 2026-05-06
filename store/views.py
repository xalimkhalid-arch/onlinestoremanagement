from django.shortcuts import render, redirect
from django.db import connection


def home(request):
    return render(request, 'store/home.html')

def contact(request):
    return render(request, 'store/contact.html')

def product_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, price, stock
            FROM store_product
            ORDER BY name ASC
        """)
        rows = cursor.fetchall()

    products = [
        {
            'id': row[0],
            'name': row[1],
            'price': row[2],
            'stock': row[3],
        }
        for row in rows
    ]
    return render(request, 'store/product_list.html',
                 {'products': products})

def product_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, description, price, stock
            FROM store_product
            WHERE id = %s
        """, [pk])
        row = cursor.fetchone()

    if not row:
        return redirect('product_list')

    product = {
        'id': row[0],
        'name': row[1],
        'description': row[2],
        'price': row[3],
        'stock': row[4],
    }

    return render(request, 'store/product_detail.html', {
        'product':product,
    })



    

# Create your views here.
