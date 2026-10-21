import uuid
from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('brands', 'Brands'),
        ('offers', 'Offers'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product_type = models.CharField(max_length=100, default='Casual Shoes')
    rating = models.PositiveSmallIntegerField(default=5)
    colors = models.CharField(max_length=200, default='Black,White,Brown')
    is_featured = models.BooleanField(default=False)
    


    def __str__(self):
        return self.name

    
    @property
    def color_list(self):
        return [
            color.strip()
            for color in self.colors.split(',')
            if color.strip()
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/gallery/')
    
    def __str__(self):
        return f"Image for {self.product.name}"


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RAZORPAY', 'Razorpay'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PLACED', 'Placed'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    order_number = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    landmark = models.CharField(max_length=200, blank=True)
    pincode = models.CharField(max_length=10)

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='PENDING'
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    product_name = models.CharField(max_length=200)

    # Save the purchase-time price, even if the product price changes later.
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
