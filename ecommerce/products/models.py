from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

GENDER_CHOICES = [
    ("Men", "Men"),
    ("Women", "Women"),
    ("Unisex", "Unisex"),
]

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Original price
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Discount price
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        default=1  # Replace 1 with an existing category ID.
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Unisex")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def has_discount(self):
        return self.discounted_price is not None
