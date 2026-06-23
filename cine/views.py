from django.shortcuts import render, redirect, get_object_or_404
from .models import Tehno
import random
import requests

def tehno_start(request):
    return render(request, 'start.html')

def tehno_register(request):
    return render(request, 'register.html')

def tehno_login(request):
    return render(request, 'login.html')

def tehno_profile(request):
    return render(request, 'profil.html')


def tehno_index(request):
    username = request.GET.get('user')

    if username:
        products = Tehno.objects.filter(owner=username)
    else:
        products = Tehno.objects.filter(owner='system')

    return render(request, 'index.html', {
        'products': products,
        'current_user': username
    })

def tehno_list(request):
    products = Tehno.objects.all()
    search = request.GET.get("search")
    category = request.GET.get("category")

    if search:
        products = products.filter(title__icontains=search)

    if category:
        products = products.filter(category=category)

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    fav = request.session.get('fav', [])
    fav_count = len(fav)

    return render(request, 'index.html', {
        'products': products,
        'cart_count': cart_count,
        'fav_count': fav_count,
        'fav': fav
    })

def tehno_detail(request, pk):
    product = get_object_or_404(Tehno, id=pk)

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    fav = request.session.get('fav', [])
    fav_count = len(fav)

    return render(request, 'tehno_detail.html', {
        'product': product,
        'cart_count': cart_count,
        'fav_count': fav_count
    })

def tehno_fav(request):
    fav = request.session.get('fav', [])
    fav_items = []

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    fav_count = len(fav)

    for product_id in fav:
        try:
            product = Tehno.objects.get(id=product_id)
            fav_items.append(product)
        except Tehno.DoesNotExist:
            continue

    return render(request, 'tehno_fav.html', {
        'fav_items': fav_items,
        'cart_count': cart_count,
        'fav_count': fav_count
    })

from django.http import JsonResponse

def fav_toggle(request, pk):
    fav = request.session.get("fav", [])

    product_id = str(pk)

    if product_id in fav:
        fav.remove(product_id)
        is_favorite = False
    else:
        fav.append(product_id)
        is_favorite = True

    request.session["fav"] = fav
    request.session.modified = True

    return JsonResponse({
        "is_favorite": is_favorite,
        "count": len(fav),
    })

def tehno_basket(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    cart_count = sum(cart.values())

    fav = request.session.get('fav', [])
    fav_count = len(fav)

    for product_id, quantity in cart.items():
        try:
            product = Tehno.objects.get(id=product_id)
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
        except Tehno.DoesNotExist:
            continue

    return render(request, 'tehno_basket.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': cart_count,
        'fav_count': fav_count
    })


def cart_add(request, pk):
    cart = request.session.get('cart', {})
    product_id = str(pk)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    product_id = str(pk)
    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('tehno_basket')


def cart_delete_item(request, pk):
    cart = request.session.get('cart', {})
    product_id = str(pk)
    if product_id in cart:
        del cart[product_id]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('tehno_basket')

def tehno_create(request):
    if request.method == 'POST':
        Tehno.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            image_url=request.POST.get('image_url'),
            category=request.POST.get('category'),
            ratting=request.POST.get('ratting')
        )
        return redirect('index')
    return render(request, 'tehno_create.html')


def tehno_edit(request, pk):
    product = get_object_or_404(Tehno, id=pk)
    if request.method == 'POST':
        product.title = request.POST.get('title')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.image_url = request.POST.get('image_url')
        product.category = request.POST.get('category')
        product.ratting = request.POST.get('ratting')
        product.save()
        return redirect('index')
    return render(request, 'tehno_edit.html', {'product': product})


def tehno_delete(request, pk):
    product = get_object_or_404(Tehno, id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('index')
    return render(request, 'tehno_delete.html', {'product': product})


def tehno_checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, quantity in cart.items():
        try:
            product = Tehno.objects.get(id=product_id)
            item_total = product.price * quantity
            total_price += item_total

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total
            })
        except Tehno.DoesNotExist:
            continue

    delivery_price = 300
    final_price = total_price + delivery_price if cart_items else 0

    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('index')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'final_price': final_price,
    })


def tehno_checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Tehno.objects.get(id=product_id)
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': item_total
            })
        except Tehno.DoesNotExist:
            continue

    delivery_price = 300
    final_price = total_price + delivery_price if cart_items else 0

    if request.method == 'POST':
        order_number = random.randint(100, 99999999)
        mockapi_url = "https://6a2fe782a7f8866418d53f42.mockapi.io/Orders"

        for item in cart_items:
            payload = {
                "product": item['product'].title,
                "price": float(item['product'].price),
                "number": str(order_number),
                "img": item['product'].image_url
            }
            try:
                response = requests.post(mockapi_url, json=payload)
                response.raise_for_status()
            except requests.exceptions.RequestException:
                pass

        request.session['cart'] = {}
        request.session.modified = True

        return render(request, 'finish.html', {'order_number': order_number})

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'final_price': final_price,
    })