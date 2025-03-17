from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une Composante
class ComposanteCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComposanteSerializer
    queryset = Composante.objects.all()
    def get(self, request, *args ,**kwargs):
        composante = Composante.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(composante, request)
        serializers = GetComposanteSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des Composantes",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        programme_slug = request.data.get('programme_slug')
        try:
            programme = Programme.objects.get(slug=programme_slug)
        except Programme.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['programme'] = programme.id
        serializer = ComposanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Composante ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une Composante par son slug
class GetUpdateOrDeleteComposante(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComposanteSerializer
    queryset = Composante.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            composante = Composante.objects.get(slug=slug)
        except Composante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Composante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetComposanteSerializer(composante)
        return Response({"data" : serializer.data, "message" : "Composante lister sucées" , "code" : 200 , "success" : True}, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            composante = Composante.objects.filter(slug=slug).first()
        except Composante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Composante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not Composante:
            return Response({"data" : None, "message" : "Aucun Composante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ComposanteSerializer(composante, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Composante modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            composante = Composante.objects.get(slug=slug)
        except Composante.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Composante trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        composante.delete()
        return Response({"data" : None, "message" : "Composante a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
# Va recevoir le slug du composante et liste ses sous composant
class showSous_ComposanteByProgramme(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SousComposanteSerializer
    queryset = SousComposante.objects.all()
    def get(self, request, *args, **kwargs):
        slug_composante = kwargs.get('slug')
        sous_composante = SousComposante.objects.filter(composante__slug=slug_composante)
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(sous_composante, request)
        serializers = SousComposanteSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des sous composantes d'une composante",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)

        
        