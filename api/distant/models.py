from django.db import models

class Transaction(models.Model):
    nom = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)  # date auto au moment de la création
    type_mouvement = models.CharField(max_length=50, default='Achat')
    quantite = models.IntegerField()
    categorie = models.CharField(max_length=100)
    prix_avant_promo = models.FloatField(default=0.0)
    remise = models.FloatField(default=0.0)
    prix_unitaire = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return f"{self.nom} - {self.date}"