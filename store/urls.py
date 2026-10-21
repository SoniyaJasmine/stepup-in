
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Razorpay payment URLs
    path(
        'create-razorpay-order/',
        views.create_razorpay_order,
        name='create_razorpay_order'
    ),
    path(
        'verify-razorpay-payment/',
        views.verify_razorpay_payment,
        name='verify_razorpay_payment'
    ),
    path(
    'calculate-checkout-total/',
    views.calculate_checkout_total,
    name='calculate_checkout_total'
    ),

    path('order-success/', views.order_success, name='order_success'),
    path('track-order/', views.track_order, name='track_order'),
    path('view-order/', views.view_order, name='view_order'),

    path('category/<slug:category>/', views.category, name='category'),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='store/password_reset.html'
        ),
        name='password_reset'
    ),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
]
