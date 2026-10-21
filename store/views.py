
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product


CATEGORIES = [
    {'name': 'Women', 'slug': 'women'},
    {'name': 'Men', 'slug': 'men'},
    {'name': 'Kids', 'slug': 'kids'},
    {'name': 'Brands', 'slug': 'brands'},
    {'name': 'Offers', 'slug': 'offers'},
]


def common_context():
    return {'categories': CATEGORIES}


def home(request):
    products = Product.objects.filter(
        is_available=True,
        is_featured=True
    )[:8]

    context = common_context()
    context['products'] = products
    return render(request, 'store/home.html', context)


def about(request):
    return render(request, 'store/about.html', common_context())


def contact(request):
    return render(request, 'store/contact.html', common_context())


def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = None

        if user:
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )
        else:
            authenticated_user = None

        if authenticated_user is not None:
            auth_login(request, authenticated_user)
            messages.success(request, 'Login successful!')
            return redirect('home')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'store/login.html', common_context())


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        agree_terms = request.POST.get('agree_terms')


        if not name or not email or not password:
            messages.error(request, 'Please fill in all required fields.')

        elif User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'This email is already registered.')

        elif agree_terms != 'on':
            messages.error(request, 'Please agree to the Terms and Conditions.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif len(password) < 8:
            messages.error(
                request,
                'Password must contain at least 8 characters.'
            )

        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            messages.success(
                request,
                'Registration successful! Please log in.'
            )
            return redirect('login')

    return render(request, 'store/register.html', common_context())


def cart(request):
    return render(request, 'store/cart.html', common_context())

def checkout(request):
    return render(request, 'store/checkout.html', common_context())

def order_success(request):
    return render(
        request,
        'store/order_success.html',
        common_context()
    )

def track_order(request):
    return render(
        request,
        'store/order_tracking.html',
        common_context()
    )

def view_order(request):
    return render(
        request,
        'store/view_order.html',
        common_context()
    )

def category(request, category):
    category_slug = category.lower()

    if category_slug not in ['men', 'women', 'kids', 'offers']:
        return redirect('home')

    if category_slug == 'offers':
        products = Product.objects.filter(is_available=True)
    else:
        products = Product.objects.filter(is_available=True, category=category_slug)

    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    sort_by = request.GET.get('sort', 'featured')

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            min_price = ''

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            max_price = ''

    if request.GET.get('in_stock') == 'on':
        products = products.filter(stock__gt=0)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    elif sort_by == 'featured':
        products = products.order_by('-is_featured', '-created_at')
    else:
        products = products.order_by('-created_at')

    context = common_context()
    context.update({
        'category': category_slug.title(),
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
        'in_stock': request.GET.get('in_stock') == 'on',
    })

    return render(request, 'store/category.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    context = common_context()
    context['product'] = product

    return render(request, 'store/product_detail.html', context)

