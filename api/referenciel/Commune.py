from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une commune
class CommuneCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommuneSerializer
    queryset = Commune.objects.all()
    def get(self, request, *args ,**kwargs):
        commune = Commune.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(commune, request)
        serializers = CommuneSerializer(result_page, many=True)
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
        departement_slug = request.data.get('departement_slug')
        try:
            departement = Departement.objects.get(slug=departement_slug)
        except Departement.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Departement trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['departement'] = departement.id
        serializer = CommuneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Commune ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une commune par son slug
class GetUpdateOrDeleteCommune(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommuneSerializer
    queryset = Commune.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            commune = Commune.objects.get(slug=slug)
        except Commune.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun commune trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommuneSerializer(commune)
        return Response({"data" : serializer.data, "message" : "Commune ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            commune = Commune.objects.filter(slug=slug).first()
        except Commune.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun commune trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not commune:
            return Response({"data" : None, "message" : "Aucun commune trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommuneSerializer(commune, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Commune modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            commune = Commune.objects.get(slug=slug)
        except Commune.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun commune trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        commune.delete()
        return Response({"data" : None, "message" : "Commune a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
