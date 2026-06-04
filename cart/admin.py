from django.contrib import admin

from cart.models import Cart, CartItem

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = ('user__username', 'product__name')
    class Meta:
        model = CartItem
        search_fields = ['cart__user__username', 'product__name']
        