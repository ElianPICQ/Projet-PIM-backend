from django.db import models

# Create your models here.
class StockProduct(models.Model):
    # Keeps the id coming from the original products source.
    original_product_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=127)
    quantity = models.IntegerField()
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    comments = models.CharField(max_length=255, default="")
    supplier = models.CharField(max_length=127)