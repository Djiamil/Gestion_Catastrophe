from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .valeur import *

class FicheDeCollecteDonnees(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FicheCollecteDonneeSerializer
    queryset = FicheCollecteDonnee.objects.all()
    def get(self, request, *args ,**kwargs):
        ficheCollecteDonnee = FicheCollecteValeur.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(ficheCollecteDonnee, request)
        serializers = GetFicheCollecteDonneeSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des Données a collecter",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        slug_configuiration = request.data.get("slug_configuiration")
        try:
            configuration = FicheCollecteConfiguration.objects.get(slug=slug_configuiration)
        except FicheCollecteConfiguration.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun onfiguiration pour cette données de collectes"})
        request.data['configuration'] = configuration.id
        serializer = FicheCollecteDonneeSerializer(data=request.data)
        if serializer.is_valid():
            donnee = serializer.save()
            pre_remplir_valeurs(donnee)
            return Response({"data" : serializer.data, "message" : "Configuiration fiche de collecte ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)