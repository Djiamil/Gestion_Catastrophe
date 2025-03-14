from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination



# views pour enregistre une Projet
class ProjetCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjetSerializer
    queryset = Projet.objects.all()
    def get(self, request, *args ,**kwargs):
        projet = Projet.objects.all()
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(projet, request)
        serializers = GetProjetSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des Projets",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        composante_slug = request.data.get('composante_slug')
        programme_slug = request.data.get('programme_slug')
        sous_composante_slug = request.data.get('sous_composante_slug')

        # Vérifier si au moins une des Foreign Keys est fournie
        if not composante_slug and not programme_slug and not sous_composante_slug:
            return Response(
                {"data": None, "message": "Au moins une composante, programme ou sous-composante doit être fournie", "code": 400, "success": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer la composante si elle est fournie
        if composante_slug:
            try:
                composante = Composante.objects.get(slug=composante_slug)
                request.data['composante'] = composante.id
            except Composante.DoesNotExist:
                return Response({"data": None, "message": "Aucune composante trouvée", "code": 404, "success": False}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer le programme si il est fourni
        if programme_slug:
            try:
                programme = Programme.objects.get(slug=programme_slug)
                request.data['programme'] = programme.id
            except Programme.DoesNotExist:
                return Response({"data": None, "message": "Aucun programme trouvé", "code": 404, "success": False}, status=status.HTTP_404_NOT_FOUND)

        # Récupérer la sous-composante si elle est fournie
        if sous_composante_slug:
            try:
                sous_composante = SousComposante.objects.get(slug=sous_composante_slug)
                request.data['sous_composante'] = sous_composante.id
            except SousComposante.DoesNotExist:
                return Response({"data": None, "message": "Aucune sous-composante trouvée", "code": 404, "success": False}, status=status.HTTP_404_NOT_FOUND)

        # Sérialiser les données et enregistrer le projet
        serializer = ProjetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": serializer.data, "message": "Projet ajouté avec succès", "code": 201, "success": True},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"data": serializer.errors, "message": "Erreur de validation", "code": 400, "success": False},
            status=status.HTTP_400_BAD_REQUEST
        )
    
# viewspour modifier suprimer ou lister une Projet par son slug
class GetUpdateOrDeleteProjet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjetSerializer
    queryset = Projet.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            projet = Projet.objects.get(slug=slug)
        except Projet.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Projet trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetProjetSerializer(projet)
        return Response({"data" : serializer.data, "message" : "Projet lister sucées" , "code" : 200 , "success" : True}, status=status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            projet = Projet.objects.filter(slug=slug).first()
        except Projet.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Projet trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not Projet:
            return Response({"data" : None, "message" : "Aucun Projet trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjetSerializer(projet, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "Projet modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try :
            projet = Projet.objects.get(slug=slug)
        except Projet.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun Projet trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        projet.delete()
        return Response({"data" : None, "message" : "Projet a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)

        
        