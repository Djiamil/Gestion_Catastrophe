from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une Programme
class ProgrammeCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetProgrammeSerializer
    queryset = Programme.objects.all()
    def get(self, request, *args ,**kwargs):
        programme = Programme.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(programme, request)
        serializers = GetProgrammeSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des programmes",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        bailleur_slug = request.data.get('bailleur_slug')
        try:
            bailleur = Bailleur.objects.get(slug=bailleur_slug)
        except Region.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun bailleur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        request.data['bailleur'] = bailleur.id
        serializer = ProgrammeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Programme ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une Programme par son slug
class GetUpdateOrDeleteProgramme(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgrammeSerializer
    queryset = Programme.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            programme = Programme.objects.get(slug=slug)
        except Programme.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetProgrammeSerializer(programme)
        return Response({"data" : serializer.data, "message" : "Programme lister sucées" , "code" : 200 , "success" : True}, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            programme = Programme.objects.filter(slug=slug).first()
        except Programme.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not programme:
            return Response({"data" : None, "message" : "Aucun Programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProgrammeSerializer(programme, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Programme modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            programme = Programme.objects.get(slug=slug)
        except Programme.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        programme.delete()
        return Response({"data" : None, "message" : "Programme a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

# Va recevoir le slug du programe et liste ses composantes
class showComponsateByProgramme(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ComposanteSerializer
    queryset = Composante.objects.all()
    def get(self, request, *args, **kwargs):
        slug_programme = kwargs.get('slug')
        composante = Composante.objects.filter(programme__slug=slug_programme)
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(composante, request)
        serializers = ComposanteSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des composantes d'un programme",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)

            
