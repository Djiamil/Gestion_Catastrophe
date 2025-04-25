from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class FicheDeCollecteConfiguiration(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FicheCollecteConfigurationSerializer
    queryset = FicheCollecteConfiguration.objects.all()
    def get(self, request, *args ,**kwargs):
        ficheCollecteConfiguration = FicheCollecteConfiguration.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(ficheCollecteConfiguration, request)
        serializers = FicheCollecteConfigurationSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des configuiration de fiche de collecte",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        serializer = FicheCollecteConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Configuiration fiche de collecte ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)