from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from api.serializers import IndicateurSerializer





# views pour enregistre une Indicateur
class IndicateurCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndicateurSerializer
    queryset = Indicateur.objects.all()
    def get(self, request, *args ,**kwargs):
        indicateur = Indicateur.objects.all().order_by('-created_at')
        
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(indicateur, request)
        
        serializers = GetIndicateurSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des Indicateurs",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        unite_slug = request.data.get('unite_mesure')
        type_indicateur_slug = request.data.get('type_indicateur')
        try:
            unite = UniteMesure.objects.get(slug=unite_slug)
        except UniteMesure.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun unité trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['unite_mesure'] = unite.id
        try:
            type_indicateur = TypeDindicateur.objects.get(slug=type_indicateur_slug)
        except Region.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Type d'indicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['type_indicateur'] = type_indicateur.id
        serializer = IndicateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Indicateur ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une Indicateur par son slug
class GetUpdateOrDeleteIndicateur(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndicateurSerializer
    queryset = Indicateur.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            indicateur = Indicateur.objects.get(slug=slug)
        except Indicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Indicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = IndicateurSerializer(indicateur)
        return Response({"data" : serializer.data, "message" : "Indicateur ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            indicateur = Indicateur.objects.filter(slug=slug).first()
        except Indicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Indicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not Indicateur:
            return Response({"data" : None, "message" : "Aucun Indicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = IndicateurSerializer(indicateur, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Indicateur modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            indicateur = Indicateur.objects.get(slug=slug)
        except Indicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Indicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        indicateur.delete()
        return Response({"data" : None, "message" : "Indicateur a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        
        

            
        

