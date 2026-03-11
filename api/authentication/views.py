from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class Register(APIView):

    def post(self, request, format=None):
        user = UserSerializer(data=request.data)

        if user.is_valid():
            user.save()
            refresh = RefreshToken.for_user(user.instance)
#            refresh["username"] = user.instance.username
            return Response({
                "success": "true",
                "message": "Login success",
                "user": user.data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_201_CREATED)
        
        return Response({"success": "false", "message": "Register failed", "errors": user.errors}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    def post(self, request, format=None):
        try:
            user = User.objects.get(username=request.data["username"])
        except User.DoesNotExist:
            return Response({"success": "false", "message": "Login failed 1: Wrong credentials"})

        if user and user.check_password(request.data["password"]):
            refresh = RefreshToken.for_user(user)
#            refresh["username"] = user.username
            return Response({
                "success": "true",
                "message": "Login success",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        
        return Response({"success": "false", "message": "Login failed 2: Wrong credentials"})

class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        try:
            refresh_token = request.data.get("refresh")
            
            if refresh_token:
                RefreshToken(refresh_token).blacklist()
            
            return Response({
                "success": "true",
                "message": "Logout successful"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": "false",
                "message": f"Logout failed: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
