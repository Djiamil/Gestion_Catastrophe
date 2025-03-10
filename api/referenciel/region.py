from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination




# views pour enregistre une region
class RegionCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    def get(self, request, *args ,**kwargs):
        region = Region.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(region, request)
        serializers = RegionSerializer(result_page, many=True)
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
        serializer = RegionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Region ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 422 , "success" : False}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
# viewspour modifier suprimer ou lister une region par son slug
class GetUpdateOrDeleteRegion(generics.ListCreateAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            region = Region.objects.get(slug=slug)
        except Region.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun region trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegionSerializer(region)
        return Response({"data" : serializer.data, "message" : "Region ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            region = Region.objects.filter(slug=slug).first()
        except Region.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun region trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not region:
            return Response({"data" : None, "message" : "Aucun region trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegionSerializer(region, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Region modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            region = Region.objects.get(slug=slug)
        except Region.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun region trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        region.delete()
        return Response({"data" : None, "message" : "Region a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        

            
        

