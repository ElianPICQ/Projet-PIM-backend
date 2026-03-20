from django.db import models

# Create your models here.
class StockProduct(models.Model):
    # Keeps the id coming from the original products source.
    original_product_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=127)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, default='kg')
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    comments = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=127, default="")