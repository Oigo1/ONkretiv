from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from .models import *

# Create your views here.

def main(request):
    context = {}
    return render(request, "store/main.html", context)


def ONkretiv(request):
    categories = ProductCategory.objects.all()
    special_categories = SpecialCategory.objects.all()
    context = {
        'categories': categories,
        'special_categories': special_categories,
    }
    return render(request, 'store/ONkretiv.html', context)



def products_by_category(request, category_type, category_name):
    if category_type == 'special':
        category = get_object_or_404(SpecialCategory, name=category_name)
        products = Product.objects.filter(special_category=category)
    else:
        category = get_object_or_404(ProductCategory, name=category_name)
        products = Product.objects.filter(category=category)
    return render(request, 'store/products_by_category.html', {'category': category, 'products': products})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_price = sum(item.total_price for item in items)
        total_items = sum(item.quantity for item in items)
        show_checkout = True
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        order, created = Order.objects.get_or_create(session_key=session_key, complete=False)
        items = order.orderitem_set.all()
        total_price = sum(item.total_price for item in items)
        total_items = sum(item.quantity for item in items)
        show_checkout = False

    context = {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
        'show_checkout': show_checkout,
    }

    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_price = sum(item.total_price for item in items)
        total_items = sum(item.quantity for item in items)
    else:
        cart = request.session.get('cart', {})
        items = []
        total_price = 0
        total_items = 0
        for product_id, item_data in cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item_data['quantity']
            total_price += product.price * quantity
            total_items += quantity
            items.append({
                'id': product_id,
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity,
            })

    context = {
        'items': items,
        'total_price': total_price,
        'total_items': total_items,
    }
    print(context)

    return render(request, "store/checkout.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/info_page.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if not created:
            order_item.quantity += 1
        order_item.save()
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        order, created = Order.objects.get_or_create(session_key=session_key, complete=False)
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        if not created:
            order_item.quantity += 1
        order_item.save()

    return redirect('cart')


def update_cart_item(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(OrderItem, id=cart_item_id)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        # Recalculate the total items and total price
        order = cart_item.order
        total_items = sum(item.quantity for item in order.orderitem_set.all())
        total_price = sum(item.product.price * item.quantity for item in order.orderitem_set.all())

        return JsonResponse({'status': 'success', 'total_items': total_items, 'total_price': total_price})
    return JsonResponse({'status': 'fail'})


def signup(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        gender = request.POST.get('gender', 'N')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user=user, full_name=full_name, email=email, phone_number=phone_number, gender=gender)
        auth_login(request, user)
        return redirect('main')

    return render(request, "store/signup.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('ONkretiv')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
    return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login URL



def company(request):
    context = {}
    return render(request, "store/company.html", context)


def shoes(request):
    context = {}
    return render(request, "store/shoes.html", context)

def pants(request):
    context = {}
    return render(request, "store/pants.html", context)

def tshirt(request):
    context = {}
    return render(request, "store/tshirt.html", context)

def jackets(request):
    context = {}
    return render(request, "store/jackets.html", context)

def limited(request):
    context = {}
    return render(request, "store/limited.html", context)

def discount(request):
    context = {}
    return render(request, "store/discount.html", context)



def launch(request):
    context = {}
    return render(request, "store/launch.html", context)

def creative(request):
    context = {}
    return render(request, "store/creative.html", context)

def checkout(request):
    context = {}
    return render(request, "store/checkout.html", context)
