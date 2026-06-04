from django.db import models
from django.contrib.auth.models import User
from products.models import Product
class Cart(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product, through='CartItem')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Cart of  {self.user.username}"
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    @property
    def total_price(self):
        return self.product.price * self.quantity
    class Meta:
        unique_together = ('cart', 'product')
    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
