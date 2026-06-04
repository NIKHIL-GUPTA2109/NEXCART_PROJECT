from django.contrib import admin

from wishlist.models import Wishlist

# Register your models here.
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('added_at',)