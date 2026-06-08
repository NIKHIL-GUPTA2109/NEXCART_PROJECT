from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    name= models.CharField(max_length=255)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to='product_images/')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Laptops', 'Laptops'),
        ('Wearables', 'Wearables'),
        ('Fashion', 'Fashion'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Electronics',
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.name

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'product'
                ],
                name='unique_review_per_user'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    