
from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'is_available',
        'created_at',
    )

    list_filter = ('category', 'is_available')
    search_fields = ('name',)
    list_editable = ('price', 'stock', 'is_available')
    ordering = ('-created_at',)

    # Display extra image upload fields inside Product
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
