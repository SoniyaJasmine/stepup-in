import json
import razorpay

from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
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



@require_POST
@csrf_protect
def calculate_checkout_total(request):
    try:
        data = json.loads(request.body)
        items = data.get('items', [])

        if not isinstance(items, list) or not items or len(items) > 50:
            return JsonResponse(
                {'error': 'Invalid or empty cart.'},
                status=400
            )

        total = Decimal('0.00')
        validated_items = []

        for item in items:
            if not isinstance(item, dict):
                return JsonResponse(
                    {'error': 'Invalid cart item.'},
                    status=400
                )

            product_id = int(item.get('product_id', 0))
            quantity = int(item.get('quantity', 0))

            if product_id <= 0 or quantity < 1 or quantity > 10:
                return JsonResponse(
                    {'error': 'Invalid product or quantity.'},
                    status=400
                )

            product = Product.objects.filter(
                id=product_id,
                is_available=True
            ).first()

            if product is None:
                return JsonResponse(
                    {'error': 'A selected product is unavailable.'},
                    status=400
                )

            if product.stock < quantity:
                return JsonResponse(
                    {'error': f'Insufficient stock for {product.name}.'},
                    status=400
                )

            # Use the price from Django's database.
            item_total = product.price * quantity
            total += item_total

            validated_items.append({
                'product_id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'item_total': str(item_total),
            })

        return JsonResponse({
            'items': validated_items,
            'total': str(total),
            'currency': 'INR',
        })

    except (ValueError, TypeError, AttributeError, json.JSONDecodeError):
        return JsonResponse(
            {'error': 'Invalid checkout data.'},
            status=400
        )


@require_POST
@csrf_protect
def create_razorpay_order(request):
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse(
            {'error': 'Online payments are not configured.'},
            status=503
        )

    try:
        data = json.loads(request.body)
        amount = Decimal(str(data.get('amount', '0')))

        # Validate the amount before creating a payment order.
        if not amount.is_finite() or amount <= 0:
            return JsonResponse(
                {'error': 'Invalid payment amount.'},
                status=400
            )

        if amount > Decimal('1000000'):
            return JsonResponse(
                {'error': 'Order amount exceeds the allowed limit.'},
                status=400
            )

        # IMPORTANT:
        # This is a demonstration step. Before accepting real payments,
        # calculate the total from trusted server-side product prices,
        # quantities and stock—not the browser's amount.
        amount_paise = int(amount * 100)

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        order = client.order.create({
            'amount': amount_paise,
            'currency': 'INR',
            'receipt': f'stepup_{request.session.session_key or "checkout"}'
        })

        return JsonResponse({
            'key_id': settings.RAZORPAY_KEY_ID,
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
        })

    except (ValueError, TypeError, InvalidOperation, json.JSONDecodeError):
        return JsonResponse(
            {'error': 'Invalid request data.'},
            status=400
        )
    except Exception:
        # Log the exception privately on the server when debugging.
        return JsonResponse(
            {'error': 'Unable to create payment order. Please try again.'},
            status=502
        )


@require_POST
@csrf_protect
def verify_razorpay_payment(request):
    if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        return JsonResponse(
            {'error': 'Online payments are not configured.'},
            status=503
        )

    try:
        data = json.loads(request.body)

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        client.utility.verify_payment_signature({
            'razorpay_order_id': data.get('razorpay_order_id', ''),
            'razorpay_payment_id': data.get('razorpay_payment_id', ''),
            'razorpay_signature': data.get('razorpay_signature', ''),
        })

        # Signature verification confirms the callback signature.
        # A production checkout must also validate the stored order,
        # amount, currency and payment status on the server before
        # marking the order as paid.
        return JsonResponse({
            'verified': True,
            'message': 'Payment signature verified.'
        })

    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse(
            {'error': 'Invalid payment verification data.'},
            status=400
        )
    except Exception:
        return JsonResponse(
            {'error': 'Payment verification failed.'},
            status=400
        )
