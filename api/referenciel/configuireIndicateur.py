from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ..Collecte import *



# views pour enregistre une ProgrammeIndicateur
class ProgrammeIndicateurCreateOrListe(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConfiguirationIndicateurSerializer
    queryset = ProgrammeIndicateur.objects.all()
    def post(self, request, *args, **kwargs):
        indicateur_slug = request.data.get('indicateur_slug')
        programme_slug = request.data.get('programme_slug')
        periodicite = request.data.get('periodicite')
        try:
            indicateur = Indicateur.objects.get(slug=indicateur_slug)
        except Indicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun indicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        try:
            programme = Programme.objects.get(slug=programme_slug)
        except Programme.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        exists = ProgrammeIndicateur.objects.filter(indicateur=indicateur, programme=programme).exists()
        if exists:
            return Response({"data" : None, "message" : "Ce lien existe déjà" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        
        program_indicateur = ProgrammeIndicateur.objects.create(
            indicateur = indicateur,
            programme = programme,
            periodicite = periodicite
        )
        generer_collectes_pour_annee(indicateur,periodicite)
        serializer = ConfiguirationIndicateurSerializer(program_indicateur)
        return Response({"data" : serializer.data ,"message" : "Indicateur affecter au programe avec succées" ,"success" : True, "code" : 201}, status=status.HTTP_201_CREATED)

            

    
# viewspour modifier suprimer ou lister une ProgrammeIndicateur par son slug
class GetUpdateOrDeleteProgrammeIndicateur(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndicateurSerializer
    queryset = ProgrammeIndicateur.objects.all()
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try : 
            programme_indicateurs = ProgrammeIndicateur.objects.filter(programme__slug=slug)
        except ProgrammeIndicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun programme trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        indicateurs = [programme_indicateur.indicateur for programme_indicateur in programme_indicateurs]
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(indicateurs, request)
        
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

class updateConfiguiration(generics.CreateAPIView):
    def put(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            programmeIndicateur = ProgrammeIndicateur.objects.get(slug=slug)
        except ProgrammeIndicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun ProgrammeIndicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        if not ProgrammeIndicateur:
            return Response({"data" : None, "message" : "Aucun ProgrammeIndicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConfiguirationIndicateurSerializer(programmeIndicateur, data=request.data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response({"data" : serializer.data, "message" : "ProgrammeIndicateur modifier avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
        else : 
            return Response({"data" : None, "message" : serializer.errors , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)

class GetOnConfiguiration(generics.ListAPIView):
    serializer_class = GetConfiguirationIndicateurSerializer
    queryset = ProgrammeIndicateur.objects.all()
    def post(self, request, *args, **kwargs):
        slug_indicateur = kwargs.get('slug')
        slug_programme = request.data.get("slug_programme")
        try:
            programmeIndicateur = ProgrammeIndicateur.objects.get(indicateur__slug=slug_indicateur,programme__slug=slug_programme)
        except ProgrammeIndicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun ProgrammeIndicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetConfiguirationIndicateurSerializer(programmeIndicateur)
        return Response({"data" : serializer.data, "message" : "ProgrammeIndicateur lister avec sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
    def delete(self, request, *args, **kwargs):
        slug_indicateur = kwargs.get('slug')
        slug_programme = request.data.get("slug_programme")
        try :
            programmeIndicateur = ProgrammeIndicateur.objects.get(indicateur__slug=slug_indicateur,programme__slug=slug_programme)
        except ProgrammeIndicateur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun ProgrammeIndicateur trouver" , "code" : 404 , "success" : False}, status=status.HTTP_404_NOT_FOUND)
        programmeIndicateur.delete()
        return Response({"data" : None, "message" : "ProgrammeIndicateur a ete supprimer sucées" , "code" : 201 , "success" : True}, status=status.HTTP_201_CREATED)
