from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une Periode
class PeriodeCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PeriodeSerializer
    queryset = Periode.objects.all()
    def get(self, request, *args ,**kwargs):
        periode = Periode.objects.all().order_by('-created_at')
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(periode, request)
        serializers = PeriodeSerializer(result_page, many=True)
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
        serializer = PeriodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Periode ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
    
# viewspour modifier suprimer ou lister une Periode par son slug
class GetUpdateOrDeletePeriode(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PeriodeSerializer
    queryset = Periode.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            periode = Periode.objects.get(slug=slug)
        except Periode.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Periode trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = PeriodeSerializer(periode)
        return Response({"data" : serializer.data, "message" : "Periode ajouter avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            periode = Periode.objects.filter(slug=slug).first()
        except Periode.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Periode trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not Periode:
            return Response({"data" : None, "message" : "Aucun Periode trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = PeriodeSerializer(periode, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Periode modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            periode = Periode.objects.get(slug=slug)
        except Periode.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Periode trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        periode.delete()
        return Response({"data" : None, "message" : "Periode a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        
        

            
        

