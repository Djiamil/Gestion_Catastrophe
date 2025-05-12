from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.utils.timezone import make_aware
from rest_framework.views import APIView
from datetime import datetime, timedelta
import locale
from collections import defaultdict









# Views pour ajouter une valeurs par periode
class CollectionValueRecord(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollecteSerializer
    queryset = Collecte.objects.all()

    def parse_date_safe(self, date_str):
        try:
            naive_dt = datetime.strptime(date_str, "%Y-%m-%d")
            return make_aware(naive_dt)
        except Exception:
            raise ValueError("Format de date invalide. Utilisez YYYY-MM-DD.")

    def post(self, request, *args, **kwargs):
        indicateur_slug = kwargs.get("slug")
        programme_slug = request.data.get("programme_slug")
        valeur = request.data.get("valeur")
        date_debut_str = request.data.get("date_debut")
        date_fin_str = request.data.get("date_fin")

        # ✅ Conversion sécurisée en datetime (pas .date())
        try:
            date_debut = self.parse_date_safe(date_debut_str)
            date_fin = self.parse_date_safe(date_fin_str)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Comparaison logique des dates
        if date_debut > date_fin:
            return Response({"message": "La date de début ne peut pas être après la date de fin."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            programme_indicateur = ProgrammeIndicateur.objects.get(
                indicateur__slug=indicateur_slug,
                programme__slug=programme_slug
            )
        except ProgrammeIndicateur.DoesNotExist:
            return Response({"message": "Cet indicateur n'est lié à aucun programme."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Calcul durée
        delta = (date_fin.date() - date_debut.date()).days + 1

        duree_max = {
            "Journalier": 1,
            "Hebdomadaire": 7,
            "Mensuel": 31,
            "Trimestriel": 92,
            "Semestriel": 183,
            "Annuel": 366
        }.get(programme_indicateur.periodicite)

        if duree_max is None:
            return Response({"message": "Périodicité inconnue."}, status=status.HTTP_404_NOT_FOUND)

        if delta > duree_max:
            return Response({
                "message": f"La durée dépasse la limite autorisée pour la périodicité '{programme_indicateur.periodicite}'."
            }, status=status.HTTP_404_NOT_FOUND)

        collecte_existante = Collecte.objects.filter(
            indicateur=programme_indicateur.indicateur,
            date_debut=date_debut,
            date_fin=date_fin
        ).exists()

        if collecte_existante:
            return Response({"message": "Une collecte existe déjà pour cette période."}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Création sans passer date_collecte si auto_now_add=True
        collecte = Collecte.objects.create(
            indicateur=programme_indicateur.indicateur,
            valeur=valeur,
            date_debut=date_debut,
            date_fin=date_fin
        )

        return Response({
            "message": "Collecte enregistrée avec succès.",
            "data": CollecteSerializer(collecte).data,
            "success" : True,
            "code" : 201
        }, status=status.HTTP_201_CREATED)

class GetCollecteForIndicateur(APIView):
    def post(self, request, *args, **kwargs):
        indicateur_slug = kwargs.get("slug")
        programme_slug = request.data.get("programme_slug")
        periode = request.data.get("periode")

        # Récupération de la configuration de l'indicateur
        try:
            programme_indicateur = ProgrammeIndicateur.objects.get(
                indicateur__slug=indicateur_slug,
                programme__slug=programme_slug
            )
        except ProgrammeIndicateur.DoesNotExist:
            return Response({
                "data": None,
                "message": "Aucune configuration pour cet indicateur.",
                "success": False,
                "code": 404
            }, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de l'indicateur
        try:
            indicateur = Indicateur.objects.get(slug=indicateur_slug)
        except Indicateur.DoesNotExist:
            return Response({
                "data": None,
                "message": "Indicateur introuvable.",
                "success": False,
                "code": 404
            }, status=status.HTTP_400_BAD_REQUEST)

        # Récupération des collectes associées
        collectes = Collecte.objects.filter(indicateur=indicateur, periode=periode).order_by('date_debut')

        if not collectes.exists():
            generer_collectes_pour_annee(indicateur, programme_indicateur.periodicite, periode)
            collectes = Collecte.objects.filter(indicateur=indicateur, periode=periode).order_by('date_debut')

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(collectes, request)

        # Sérialisation
        serializers = GetCollecteSerializer(result_page, many=True)
        
        paginated_response = paginator.get_paginated_response(serializers.data)
        # Réponse
        # On modifie son contenu (ajout d'infos supplémentaires)
        paginated_response.data['periodicite_collecte'] = programme_indicateur.periodicite
        paginated_response.data['libelle_indicateur'] = indicateur.libelle
        paginated_response.data['message'] = "Liste des collectes récupérée avec succès."
        paginated_response.data['success'] = True
        paginated_response.data['code'] = 200

        # On retourne la réponse DRF
        return paginated_response

class CollecteUpdate(generics.UpdateAPIView):
    serializer_class = CollecteSerializer
    queryset = Collecte.objects.all()

    def put(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        valeur = request.data.get("valeur")
        valeur_prevu = request.data.get("valeur_prevu")
        periode = request.data.get("periode")

        try:
            collecte = Collecte.objects.get(slug=slug)
        except Collecte.DoesNotExist:
            return Response({
                "data": None,
                "message": "Aucun collecte trouvé",
                "success": False,
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        valeur = float(valeur)
        if collecte.valeur_prevu and valeur > collecte.valeur_prevu:
            return Response({
                "data": None,
                "message": f"La valeur réelle ne peut pas dépasser la valeur prévue qui est {collecte.valeur_prevu}",
                "success": False,
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        collecte.valeur = valeur
        collecte.valeur_prevu = valeur_prevu
        collecte.periode = periode
        collecte.save()

        serializer = self.get_serializer(collecte)
        return Response({
            "data": serializer.data,
            "message": "Valeur modifiée avec succès",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)

        
class DeleteAllCollecte(APIView):
    serializer_class = CollecteSerializer
    queryset = Collecte.objects.all()
    def delete(self, request, *args, **kwargs):
        Collecte.objects.all().delete()
        return Response({'message': 'Toutes les collectes ont été supprimées.'})
    
def generer_collectes_pour_annee(indicateur, periodicite, periode=None, annee=datetime.now().year):
    collectes = []

    if periodicite == "Journalier":
        current = datetime(annee, 1, 1)
        while current.year == annee:
            debut = make_aware(current)
            fin = make_aware(current)
            label = f"Jour {current.strftime('%j')}"  # Jour 001 à 365/366
            collectes.append(Collecte(
                indicateur=indicateur,
                valeur=None,
                date_debut=debut,
                date_fin=fin,
                periode_label=label,
                periode = periode
            ))
            current += timedelta(days=1)

    elif periodicite == "Hebdomadaire":
        current = datetime(annee, 1, 1)
        week_number = 1
        while current.year == annee:
            debut = current
            fin = current + timedelta(days=6)
            if fin.year > annee:
                fin = datetime(annee, 12, 31)
            collectes.append(Collecte(
                indicateur=indicateur,
                valeur=None,
                date_debut=make_aware(debut),
                date_fin=make_aware(fin),
                periode_label=f"Semaine {week_number}",
                periode = periode
            ))
            current += timedelta(weeks=1)
            week_number += 1

    elif periodicite == "Mensuel":
        # Appliquer la locale française
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

        for mois in range(1, 13):
            debut = datetime(annee, mois, 1)
            if mois == 12:
                fin = datetime(annee, 12, 31)
            else:
                fin = datetime(annee, mois + 1, 1) - timedelta(days=1)
            
            # Mois en français, ex: "janvier"
            label = debut.strftime("%B").capitalize()

            collectes.append(Collecte(
                indicateur=indicateur,
                valeur=None,
                date_debut=make_aware(debut),
                date_fin=make_aware(fin),
                periode_label=label,
                periode = periode
            ))
    elif periodicite == "Trimestriel":
        trimestres = [
            ("Trimestre1", datetime(annee, 1, 1), datetime(annee, 3, 31)),
            ("Trimestre2", datetime(annee, 4, 1), datetime(annee, 6, 30)),
            ("Trimestre3", datetime(annee, 7, 1), datetime(annee, 9, 30)),
            ("Trimestre4", datetime(annee, 10, 1), datetime(annee, 12, 31)),
        ]
        for label, debut, fin in trimestres:
            collectes.append(Collecte(
                indicateur=indicateur,
                valeur=None,
                date_debut=make_aware(debut),
                date_fin=make_aware(fin),
                periode_label=label,
                periode = periode
            ))

    elif periodicite == "Semestriel":
        semestres = [
            ("Semestre1", datetime(annee, 1, 1), datetime(annee, 6, 30)),
            ("Semestre2", datetime(annee, 7, 1), datetime(annee, 12, 31)),
        ]
        for label, debut, fin in semestres:
            collectes.append(Collecte(
                indicateur=indicateur,
                valeur=None,
                date_debut=make_aware(debut),
                date_fin=make_aware(fin),
                periode_label=label,
                periode = periode
            ))

    elif periodicite == "Annuel":
        debut = datetime(annee, 1, 1)
        fin = datetime(annee, 12, 31)
        collectes.append(Collecte(
            indicateur=indicateur,
            valeur=None,
            date_debut=make_aware(debut),
            date_fin=make_aware(fin),
            periode_label=f"Année {annee}",
            periode = periode
        ))

    else:
        raise ValueError("Périodicité non reconnue.")

    # ✅ Sauvegarde en bulk pour optimiser
    Collecte.objects.bulk_create(collectes)

# views pour les stats des collecte d'un indicateur par periode exemple 2023, 2024 ...
class StatsCollecteForPeriod(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollecteSerializer
    queryset = Collecte.objects.all()

    def get(self, request, *args, **kwargs):
        indicateur_slug = kwargs.get('slug')
        print("le slug de l'indicateur", indicateur_slug)
        try:
            indicateur = Indicateur.objects.get(slug=indicateur_slug)
        except Indicateur.DoesNotExist:
            return Response({
                "data": None,
                "message": "Aucun indicateur trouver",
                "success": False,
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            collectes = Collecte.objects.filter(indicateur=indicateur)
        except Collecte.DoesNotExist:
            return Response({
                "data": None,
                "message": "Aucun collecte trouvé",
                "success": False,
                "code": 404
            }, status=status.HTTP_404_NOT_FOUND)

        # Dictionnaire pour stocker les totaux par période
        total_par_periode = defaultdict(float)

        for collecte in collectes:
            if collecte.valeur is not None:
                total_par_periode[collecte.periode] += float(collecte.valeur)

        # Formatage des résultats
        data = [
            {
                "periode": periode,
                "total": total
            }
            for periode, total in total_par_periode.items()
        ]

        return Response({
            "data": data,
            "message": "Total des collectes par période récupéré avec succès",
            "success": True,
            "code": 200
        }, status=status.HTTP_200_OK)
         
        

    