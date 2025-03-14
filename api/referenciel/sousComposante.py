from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une SousComposante
class SousComposanteCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SousComposanteSerializer
    queryset = SousComposante.objects.all()
    def get(self, request, *args ,**kwargs):
        sousComposante = SousComposante.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(sousComposante, request)
        serializers = GetSousComposanteSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des SousComposantes",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        composante_slug = request.data.get('composante_slug')
        try:
            composante = Composante.objects.get(slug=composante_slug)
        except Composante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun composante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['composante'] = composante.id
        serializer = SousComposanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "SousComposante ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une SousComposante par son slug
class GetUpdateOrDeleteSousComposante(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SousComposanteSerializer
    queryset = SousComposante.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            sousComposante = SousComposante.objects.get(slug=slug)
        except SousComposante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun SousComposante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetSousComposanteSerializer(sousComposante)
        
        return Response({"data" : serializer.data, "message" : "SousComposante lister sucées" , "code" : 200 , "success" : True}, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            sousComposante = SousComposante.objects.filter(slug=slug).first()
        except SousComposante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun SousComposante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not SousComposante:
            return Response({"data" : None, "message" : "Aucun SousComposante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = SousComposanteSerializer(sousComposante, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "SousComposante modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            sousComposante = SousComposante.objects.get(slug=slug)
        except SousComposante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun SousComposante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        sousComposante.delete()
        return Response({"data" : None, "message" : "SousComposante a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        
        