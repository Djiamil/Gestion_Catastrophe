from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


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
            
# views pour ajouter un nouveau role dans la base
class AddRole(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Role ajouté avec succès", "success": True, "code": 201},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"data": None, "message": serializer.errors, "success": False, "code": 400},
                status=status.HTTP_400_BAD_REQUEST
            )
# Views Pour ajouter un utilisateur
class AddUser(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        role_slug = request.data.get("role_slug")

        try:
            role = Role.objects.get(slug=role_slug)
        except Role.DoesNotExist:
            return Response(
                {"data": None, "message": "Veuillez attribuer un rôle à cet utilisateur", "success": False, "code": 404},
                status=status.HTTP_404_NOT_FOUND
            )
        # Créer une copie des données pour modification
        request.data['role'] = role.id

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            password = make_password(serializer.validated_data['password'])
            serializer.validated_data['password'] = password
            serializer.save()
            return Response(
                {"data": UserSerializer(serializer.data), "message": "Utilisateur ajouté avec succès", "success": True, "code": 201},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"data": None, "message": serializer.errors, "success": False, "code": 400},
                status=status.HTTP_400_BAD_REQUEST
            )