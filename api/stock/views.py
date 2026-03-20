from django.db import transaction
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockProductSerializer
from .models import StockProduct
from api.distant.serializers import TransactionSerializer


def _create_transaction_entry(product, type_mouvement):
    transaction_payload = {
        'type_mouvement': type_mouvement,
        'original_product_id': product.get('original_product_id'),
        'name': product.get('name'),
        'category': product.get('category'),
        'quantity': product.get('quantity'),
        'price': product.get('price'),
        'unit': product.get('unit'),
        'discount': product.get('discount'),
        'comments': product.get('comments', ''),
        'supplier': product.get('supplier'),
    }

    serializer = TransactionSerializer(data=transaction_payload)
    if not serializer.is_valid():
        return serializer.errors
    serializer.save()
    return None

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

                transaction_errors = _create_transaction_entry(product, 'Achat')
                if transaction_errors:
                    return Response(transaction_errors, status=status.HTTP_400_BAD_REQUEST)

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
                operation = product.get('operation')

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

                if operation is None:
                    return Response(
                        {'operation': ['This field is required.']},
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
                    quantity__gte=quantity,
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

                transaction_errors = _create_transaction_entry(product, operation)
                if transaction_errors:
                    return Response(transaction_errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Stocks processed successfully.'}, status=status.HTTP_200_OK)

class RedirectionDeleteStock(APIView):
    def post(self, request, format=None):
        row_id = request.data.get('id')

        if row_id is None:
            return Response(
                {'id': ['This field is required.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            row_id = int(row_id)
        except (TypeError, ValueError):
            return Response(
                {'id': ['A valid integer is required.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        if row_id <= 0:
            return Response(
                {'id': ['Id must be greater than 0.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        stock = StockProduct.objects.filter(id=row_id).first()
        if stock is None:
            return Response(
                {'id': ['Stock product not found.']},
                status=status.HTTP_404_NOT_FOUND
            )

        if stock.quantity > 0:
            return Response(
                {'quantity': ['Cannot delete non-empty stock.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted_item = StockProductSerializer(stock).data
        stock.delete()

        return Response(
            {
                'detail': 'Stock row deleted successfully.',
                'deleted': deleted_item,
            },
            status=status.HTTP_200_OK
        )