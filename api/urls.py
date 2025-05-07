from django.urls import path
from api.views import *
from api.referenciel.region import *
from api.referenciel.departement import *
from api.referenciel.Commune import *
from api.referenciel.uniteMesure import *
from api.referenciel.Periode import *
from api.referenciel.Bailleur import *
from api.referenciel.typeIndicateur import *
from api.referenciel.indicateur import *
from api.referenciel.programme import *
from api.referenciel.configuireIndicateur import *
from api.referenciel.composante import *
from api.referenciel.sousComposante import *
from api.referenciel.projet import *
from api.Collecte import *
from api.fiche_de_collecte.configuiration import *
from api.fiche_de_collecte.donnee import *
from api.fiche_de_collecte.valeur import *

urlpatterns = [
    # Debu des endPointe des fonction qui sont dans views 
    path('login/', LoginView.as_view(), name='login'),
    path('role_create/', AddRole.as_view(), name='create_role'),
    path('user_create/', AddUser.as_view(), name='create_user'),
    # Fin des endpoint qui sont dans views
    
    # DEBUT Url qui ourne au toure des region
    path('region_create_or_liste/', RegionCreateOrListe.as_view(), name='region_create_or_liste'),
    path('region_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteRegion.as_view(), name='region_getOn_update_delete'),
    path('region_all/', RegionAll.as_view(), name='region_all'),
    # FIN url qui tourne au toure des region  
    # Debut route qui tourne au toure du departement 
    path('departement_create_or_liste/', DepartementCreateOrListe.as_view(), name='departement_create_or_liste'),
    path('departement_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteDepartement.as_view(), name='departement_getOn_update_delete'),
    path('departement_all/', DepartementAll.as_view(), name='departement_all'),
    # Fin des route qui tourne autoure du departement
    # Deut des routes qui tourne au toure de la commune
    path('commune_create_or_liste/', CommuneCreateOrListe.as_view(), name='commune_create_or_liste'),
    path('commune_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteCommune.as_view(), name='commune_getOn_update_delete'),
    # Fin des routes qui tourne au toure de la commune
    # Debut des route pour les unité de mesure
    path('uniteMesure_create_or_liste/', UniteMesureCreateOrListe.as_view(), name='uniteMesure_create_or_liste'),
    path('uniteMesure_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteUniteMesure.as_view(), name='uniteMesure_getOn_update_delete'),
    # Fin des url pour les unité de esure
    # Debut des route pour la periode
    path('periode_create_or_liste/', PeriodeCreateOrListe.as_view(), name='periode_create_or_liste'),
    path('periode_getOn_update_delete/<slug:slug>/', GetUpdateOrDeletePeriode.as_view(), name='periode_getOn_update_delete'),
    # Fin des route pour la periode
    # Debut des url pour les bailleur
    path('bailleur_create_or_liste/', BailleurCreateOrListe.as_view(), name='bailleur_create_or_liste'),
    path('bailleur_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteBailleur.as_view(), name='bailleur_getOn_update_delete'),
    # Fin des url pour les bailler
    # Debut des endpoint pour les type d'indicateur 
    path('typeIndicateur_create_or_liste/', TypeDindicateurCreateOrListe.as_view(), name='typeIndicateur_create_or_liste'),
    path('typeIndicateur_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteTypeDindicateur.as_view(), name='typeIndicateur_getOn_update_delete'),
    # Fin des endpoint pour les type indicateur
    # Debut des endPoint pour les indicateur
    path('indicateur_create_or_liste/', IndicateurCreateOrListe.as_view(), name='typeIndicateur_create_or_liste'),
    path('indicateur_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteIndicateur.as_view(), name='typeIndicateur_getOn_update_delete'),
    # Fin des endpoint pour les indicateur
    # debu des route pour programme
    path('programme_create_or_liste/', ProgrammeCreateOrListe.as_view(), name='programme_create_or_liste'),
    path('programme_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteProgramme.as_view(), name='programme_getOn_update_delete'),
    path('programme_composante/<slug:slug>/', showComponsateByProgramme.as_view(), name='programme_composante'),
    # fin des route pour programme
    # Les endPoint qui tourne au tour du programme et de l'indicateur
    path('affect_programme_indicateur/', ProgrammeIndicateurCreateOrListe.as_view(), name='affecte_programme_indicateur'),
    path('configuire_programme_indicateur/<slug:slug>/', GetUpdateOrDeleteProgrammeIndicateur.as_view(), name='affecte_programme_indicateur'),
    path('getOnConfiguiration/<slug:slug>/', GetOnConfiguiration.as_view(), name='get_on_configuiration'),
    path('update_delete_configuiration/<slug:slug>/', updateConfiguiration.as_view(), name='update_delete_configuiration'),
    # fin es endPoint pour affecter un programme a un indicateur
    # debut des url pour les composante
    path('composante_create_or_liste/', ComposanteCreateOrListe.as_view(), name='affecte_programme_indicateur'),
    path('composante_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteComposante.as_view(), name='affecte_programme_indicateur'),
    path('sous_composante_composante/<slug:slug>/', showSous_ComposanteByProgramme.as_view(), name='sous_composante_composante'),
    # fin des url pour les composante
     # debut des url pour les souscomposante
    path('sous_composante_create_or_liste/', SousComposanteCreateOrListe.as_view(), name='affecte_programme_indicateur'),
    path('sous_composante_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteSousComposante.as_view(), name='affecte_programme_indicateur'),
    # fin des url pour les ouscomposante
    # debut des url pour les souscomposante
    path('projet_create_or_liste/', ProjetCreateOrListe.as_view(), name='affecte_programme_indicateur'),
    path('projet_getOn_update_delete/<slug:slug>/', GetUpdateOrDeleteProjet.as_view(), name='affecte_programme_indicateur'),
    path('projet_filter/', FiltreByProgrammeComposanteSousComposante.as_view(), name='projet_filter'),
    # fin des url pour les ouscomposante
    # Debut des routes pour les collectes
    path('collecte_record/<slug:slug>/', CollectionValueRecord.as_view(), name='collecte_record'),
    path('collecte_liste_by_indicateur/<slug:slug>/', GetCollecteForIndicateur.as_view(), name='collecte_liste'),
    path("collecte_update/<slug:slug>/", CollecteUpdate.as_view(), name="collecte-update"),
    path("purge_collectes/", DeleteAllCollecte.as_view(), name="collecte-delete"),
    # Fin des routes pour les collectes  
    # Debut des routes pour les fiches de collectes
    path('fiche_de_collecte_configuirations/', FicheDeCollecteConfiguiration.as_view(), name='fiche_de_collecte_configuirations'),
    path('fiche_de_collecte_donnees/', FicheDeCollecteDonnees.as_view(), name='fiche_de_collecte_configuirations'),
    path('fiche_de_collecte_valeurs/', FicheDeCollecteValeurs.as_view(), name='fiche_de_collecte_valeurs'),
    path('fiche_de_collecte_valeur/<slug:slug>/', FicheDeCollecteValeurAdd.as_view(), name='fiche_de_collecte_valeurs_add_liste'),
    # Fin des routes pour les fiches de collectes
]
# Username superuser: Djiamil
# Email address: djiamil@gmail.com
# Password: Passer123!