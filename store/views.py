from django.shortcuts import render, redirect
from django.db import connection


def home(request):
    return render(request, 'store/home.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        message = request.POST.get('message')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO store_message
                    (name, email, contact, message, 
                     created_at, is_read)
                VALUES 
                    (%s, %s, %s, %s,
                     CURRENT_TIMESTAMP, 0)
            """, [name, email, contact, message])

        return render(request, 'store/contact.html',
                     {'success': True})

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

def my_messages(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name, email, contact, 
                   message, reply, created_at
            FROM store_message
            WHERE email = %s
            ORDER BY created_at DESC
        """, [request.user.email])
        rows = cursor.fetchall()

    messages = [
        {
            'name': row[0],
            'email': row[1],
            'contact': row[2],
            'message': row[3],
            'reply': row[4],
            'created_at': row[5],
        }
        for row in rows
    ]
    return render(request, 'store/my_messages.html',
                 {'messages': messages})



    

# Create your views here.
