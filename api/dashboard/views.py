from django.shortcuts import render
from django.db.models import Sum, F, FloatField, ExpressionWrapper
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from rest_framework.response import Response
from api.stock.models import StockProduct
from api.distant.models import Transaction

class RedirectionDashboard(APIView):
    def get(self, request, format=None):
        total = StockProduct.objects.count()
        out_of_stock = StockProduct.objects.filter(quantity=0).count()
        low_stock = StockProduct.objects.filter(quantity__lt=10).count()
        total_ventes = Transaction.objects.filter(type_mouvement='Vente').aggregate(
            total=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField()))
        )['total'] or 0
        nb_achats = Transaction.objects.filter(type_mouvement='Achat').count()
        nb_ventes = Transaction.objects.filter(type_mouvement='Vente').count()
        nb_invendus = Transaction.objects.filter(type_mouvement='Invendu').count()
        ventes_par_jour = (
            Transaction.objects
            .filter(type_mouvement='Vente')
            .annotate(day=TruncDate('date'))
            .values('day')
            .annotate(value=Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=FloatField())))
            .order_by('day')
        )
        ventes_par_jour_list = [
            {'value': entry['value'], 'date': entry['day'].strftime('%d/%m/%Y')}
            for entry in ventes_par_jour
        ]
        return Response({
            'total_products': total,
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'total_ventes': total_ventes,
            'nb_achats': nb_achats,
            'nb_ventes': nb_ventes,
            'nb_invendus': nb_invendus,
            'ventes_par_jour': ventes_par_jour_list,
        })