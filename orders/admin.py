from django.contrib import admin

from orders.models import Order, ShippingAddress

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'total_price', 'is_cancelled')
    list_filter = ('created_at', 'is_cancelled')
    search_fields = ('user__username',)
@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipient_name', 'phone', 'city')
    search_fields = ('user__username', 'recipient_name', 'phone', 'city')   