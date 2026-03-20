from django.db import models

class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)  # date auto au moment de la création
    type_mouvement = models.CharField(max_length=50, default='Achat')
    original_product_id = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=127)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, default='kg')
    price = models.FloatField(default=0.0)
    discount = models.FloatField(default=0.0)
    comments = models.CharField(max_length=255, blank=True)
    supplier = models.CharField(max_length=127, default="")