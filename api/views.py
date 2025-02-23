from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            return Response({"data": None,"message": "Mot de passe incorrect","success": False,"code": 401}, status=status.HTTP_401_UNAUTHORIZED)
        # Générer un token JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "token": access_token,
            "refresh": str(refresh),
            "data": UserSerializer(user).data,
            "message": "Utilisateur authentifié avec succès",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
            
        