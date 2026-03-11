from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

import time

class Prouct(APIView):
    def get(self, request):
        time.sleep(5)
        return Response({"message": "Hello, World!"})