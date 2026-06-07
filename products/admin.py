from django.contrib import admin
from .models import Product, Review
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'category',
        'is_featured'
    ]
    search_fields = ['name', 'category']
admin.site.register(Review)