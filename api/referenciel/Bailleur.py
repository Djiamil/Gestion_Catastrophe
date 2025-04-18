from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une Bailleur
class BailleurCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BailleurSerializer
    queryset = Bailleur.objects.all()
    def get(self, request, *args ,**kwargs):
        bailleur = Bailleur.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(bailleur, request)
        serializers = BailleurSerializer(result_page, many=True)
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
        serializer = BailleurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Bailleur ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une Bailleur par son slug
class GetUpdateOrDeleteBailleur(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BailleurSerializer
    queryset = Bailleur.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            bailleur = Bailleur.objects.filter(slug=slug).first()
        except Bailleur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Bailleur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = BailleurSerializer(bailleur)
        return Response({"data" : serializer.data, "message" : "Bailleur ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            bailleur = Bailleur.objects.filter(slug=slug).first()
        except Bailleur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Bailleur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not Bailleur:
            return Response({"data" : None, "message" : "Aucun Bailleur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = BailleurSerializer(bailleur, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Bailleur modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            bailleur = Bailleur.objects.get(slug=slug)
        except Bailleur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Bailleur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        bailleur.delete()
        return Response({"data" : None, "message" : "Bailleur a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        
        

            
        

