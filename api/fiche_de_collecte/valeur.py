from ..models import *
from ..serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class FicheDeCollecteValeurs(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetFicheCollecteValeurSerializer
    queryset = FicheCollecteValeur.objects.all()
    def get(self, request, *args ,**kwargs):
        ficheCollecteValeur = FicheCollecteValeur.objects.all()
        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(ficheCollecteValeur, request)
        serializers = GetFicheCollecteValeurSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP
        return Response({
            "data": paginated_response.data,
            "message": "Liste des valeur de collecter",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
class FicheDeCollecteValeurAdd(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FicheCollecteValeurSerializer
    queryset = FicheCollecteDonnee.objects.all()
    def post(self, request, *args ,**kwargs):
        slug = kwargs.get("slug")
        periode = request.data.get("periode")
        try:
            valeur_donnees_collecte = FicheCollecteValeur.objects.filter(donnee__slug=slug,periode=periode).order_by('-date_collecte')
        except FicheCollecteValeur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun valeur de collecte trouver", "code" : 404, "status" : True}, status=status.HTTP_404_NOT_FOUND)
        if not valeur_donnees_collecte.exists():
            try:
                donnee = FicheCollecteDonnee.objects.get(slug=slug)
            except FicheCollecteDonnee.DoesNotExist:
                return Response({
                    "data": None,
                    "message": "Fiche de collecte non trouvée.",
                    "success": False,
                    "code": 404
                }, status=status.HTTP_404_NOT_FOUND)
            pre_remplir_valeurs(donnee,periode)
            valeur_donnees_collecte = FicheCollecteValeur.objects.filter(donnee__slug=slug,periode=periode).order_by('-date_collecte')

        # Ajout de la pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(valeur_donnees_collecte, request)
        serializers = GetFicheCollecteValeurSerializer(result_page, many=True)
        # Construire la réponse paginée sans utiliser le paramètre `status`
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Retourner une réponse personnalisée avec le statut HTTP 
        niveau_configuiration = valeur_donnees_collecte = FicheCollecteValeur.objects.filter(donnee__slug=slug).first()
        return Response({
            "data": paginated_response.data,
            "niveau_config" : FicheCollecteConfigurationSerializer(niveau_configuiration.donnee.configuration).data,
            "message": "Liste des valeur de collecter",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
    def put(self, request, *args ,**kwargs):
        slug = kwargs.get("slug")
        valeur = request.data.get("valeur")
        periode = request.data.get("periode")
        try:
            fiche_collecte_valeur = FicheCollecteValeur.objects.get(slug=slug)
        except FicheCollecteValeur.DoesNotExist:
            return Response({"data" : None, "message" : "Aucun valeur de collecte trouver", "code" : 404, "status" : True}, status=status.HTTP_404_NOT_FOUND)
        fiche_collecte_valeur.valeur = valeur
        fiche_collecte_valeur.periode = periode
        fiche_collecte_valeur.save()
        serializer = FicheCollecteValeurSerializer(fiche_collecte_valeur)
        return Response({
            "data": serializer.data,
            "message": "La valeur du fiche de collece a été mise a jours avec succées",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
        
    




def pre_remplir_valeurs(donnee,periode):
    configuration = donnee.configuration
    niveau = configuration.niveau

    if niveau == 'region':
        regions = Region.objects.all()
        for region in regions:
            FicheCollecteValeur.objects.create(
                donnee=donnee,
                region=region,
                periode = periode
            )

    elif niveau == 'departement':
        departements = Departement.objects.all()
        for departement in departements:
            FicheCollecteValeur.objects.create(
                donnee=donnee,
                departement=departement,
                periode = periode
            )

    elif niveau == 'commune':
        communes = Commune.objects.all()
        for commune in communes:
            FicheCollecteValeur.objects.create(
                donnee=donnee,
                commune=commune,
                periode = periode
            )