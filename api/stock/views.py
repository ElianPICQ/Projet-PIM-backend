from django.db import transaction
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockProductSerializer
from .models import StockProduct

# Create your views here.
class RedirectionGetStock(APIView):
    def get(self, request, format=None):
        stocks = StockProduct.objects.all()
        serializer = StockProductSerializer(stocks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RedirectionAddStock(APIView):
    def post(self, request, format=None):
        products = request.data.get('products')
        if not isinstance(products, list) or len(products) == 0:
            return Response(
                {'products': ['This field must be a non-empty array.']},
                status=status.HTTP_400_BAD_REQUEST
            )

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

                if quantity < 0:
                    return Response(
                        {'quantity': ['Quantity must be greater than or equal to 0.']},
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
    

class RedirectionRemoveStock(APIView):
    def post(self, request, format=None):
        products = request.data.get('products')
        if not isinstance(products, list) or len(products) == 0:
            return Response(
                {'products': ['This field must be a non-empty array.']},
                status=status.HTTP_400_BAD_REQUEST
            )

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

                if quantity < 0:
                    return Response(
                        {'quantity': ['Quantity must be greater than or equal to 0.']},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                updated_count = StockProduct.objects.filter(
                    original_product_id=original_product_id,
                ).update(
                    quantity=F('quantity') - quantity,
                )

                if updated_count == 0:
                    if not StockProduct.objects.filter(original_product_id=original_product_id).exists():
                        return Response(
                            {'original_product_id': ['Stock product not found.']},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    return Response(
                        {'quantity': ['Insufficient stock. Quantity cannot fall below 0.']},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response({'detail': 'Stocks processed successfully.'}, status=status.HTTP_200_OK)
