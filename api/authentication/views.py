from rest_framework.views import APIView
from rest_framework.response import Response

import time

from rest_framework.permissions import IsAuthenticated

""" 
from django.contrib.auth.models import User

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
 """
class Register(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        self.stdout.write('['+time.ctime()+'] Data recieved: ' + request.data)
        content = {
            'Retour1': "Je suis le 1er retour",
            'Retour2': "tkt bb ca register",
        }
        return Response(content)

class Login(APIView):

    def post(self, request, format=None):
        content = {
            'Retour1': "Je suis le 1er retour",
            'Retour2': "tkt bb ca login",
        }
        return Response(content)