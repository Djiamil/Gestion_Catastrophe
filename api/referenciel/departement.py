from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une departement
class DepartementCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartementSerializer
    queryset = Departement.objects.all()
    def get(self, request, *args ,**kwargs):
        departement = Departement.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(departement, request)
        serializers = DepartementSerializer(result_page, many=True)
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
        region_slug = request.data.get('region_slug')
        try:
            region = Region.objects.get(slug=region_slug)
        except Region.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun region trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['region'] = region.id
        serializer = DepartementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Departement ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une departement par son slug
class GetUpdateOrDeleteDepartement(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartementSerializer
    queryset = Departement.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            departement = Departement.objects.get(slug=slug)
        except Departement.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Departement trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartementSerializer(departement)
        return Response({"data" : serializer.data, "message" : "Departement ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            departement = Departement.objects.filter(slug=slug).first()
        except Departement.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun departement trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not Departement:
            return Response({"data" : None, "message" : "Aucun departement trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = DepartementSerializer(departement, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Departement modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            departement = Departement.objects.get(slug=slug)
        except Departement.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun departement trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        departement.delete()
        return Response({"data" : None, "message" : "Departement a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        
        

            
        

