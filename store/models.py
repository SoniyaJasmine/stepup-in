
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
