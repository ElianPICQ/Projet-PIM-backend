import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .config import baseUrl
from .models import Transaction
from .serializers import TransactionSerializer

class RedirectionListeDeProduits(APIView):
    def get(self, format=None):
        response = requests.get(baseUrl+'products/')
        jsondata = response.json()
        for product in jsondata:
            if 'owner' in product:
                product['supplier'] = product.pop('owner')
        return Response(jsondata)

class RedirectionDetailProduit(APIView):
    def get(self, pk, format=None):
        try:
            response = requests.get(baseUrl+'product/'+str(pk)+'/')
            jsondata = response.json()
            return Response(jsondata)
        except:
            raise Http404

class RedirectionTransactions(APIView):
    def get(self, format=None):
        all_transactions = Transaction.objects.all().order_by('-date')
        serializer = TransactionSerializer(all_transactions, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)