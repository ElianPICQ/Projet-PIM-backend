from django.db import transaction
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockProductSerializer
from .models import StockProduct

# Create your views here.
class RedirectionAddStock(APIView):
    def post(self, request, format=None):
        products = request.data.get('products')
        if not isinstance(products, list) or len(products) == 0:
            return Response(
                {'products': ['This field must be a non-empty array.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for product in products:
            print("product id = ", product.get("original_product_id"))

        with transaction.atomic():
            for product in products:
                original_product_id = product.get('original_product_id')
                quantity = product.get('quantity')

                if original_product_id is None:
                    return Response(
                        {'original_product_id': ['This field is required.']},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if quantity is None:
                    return Response(
                        {'quantity': ['This field is required.']},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                try:
                    quantity = int(quantity)
                except (TypeError, ValueError):
                    return Response(
                        {'quantity': ['A valid integer is required.']},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                updated_count = StockProduct.objects.filter(
                    original_product_id=original_product_id
                ).update(
                    quantity=F('quantity') + quantity,
                )

                if updated_count == 0:
                    create_serializer = StockProductSerializer(data=product)
                    if not create_serializer.is_valid():
                        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    create_serializer.save()

        return Response({'detail': 'Stocks processed successfully.'}, status=status.HTTP_200_OK)