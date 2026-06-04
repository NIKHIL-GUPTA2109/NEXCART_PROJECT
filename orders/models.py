from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone
# Create your models here.
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        'ShippingAddress',
        on_delete=models.SET_NULL,
        null=True
    )
    PAYMENT_CHOICES = [

    ('COD', 'Cash On Delivery'),

    ('UPI', 'UPI'),

    ('CARD', 'Card'),

    ('NETBANKING', 'Net Banking')
]

    payment_method = models.CharField(
    max_length=20,
    choices=PAYMENT_CHOICES,
    default='COD'
)
    payment_status = models.CharField(
    max_length=20,
    default='Pending'
)

    razorpay_order_id = models.CharField(
    max_length=200,
    blank=True,
    null=True
)

    payment_id = models.CharField(
    max_length=200,
    blank=True,
    null=True
)
    created_at=models.DateTimeField(default=timezone.now)
    total_price=models.DecimalField(max_digits=12,decimal_places=2)
    is_cancelled=models.BooleanField(default=False)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=12,decimal_places=2)
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
    
class ShippingAddress(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    recipient_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.recipient_name
