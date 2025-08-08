import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from safedelete.models import SafeDeleteModel
from django.contrib.auth.hashers import make_password
from django.utils import timezone




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# model ole pour la gestion des role dans la platforme
class Role(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.name
# Le medel user pour ajouter les utilisateur et la connexion se base sur cette model
class User(AbstractBaseUser, PermissionsMixin, SafeDeleteModel):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, verbose_name="Adresse Email")
    nom = models.CharField(max_length=30, blank=True, null=True, verbose_name="Nom")
    prenom = models.CharField(max_length=30, blank=True, null=True, verbose_name="Prénom")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, null=True, blank=True, verbose_name="Genre")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Avatar")
    phone_number = models.CharField(max_length=15,unique=True,null=True,blank=True, verbose_name="Numéro de téléphone")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    objects = CustomUserManager()
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.nom or self.email or "Utilisateur sans nom"

    def get_full_name(self):
        """Retourne le nom complet de l'utilisateur"""
        return f"{self.prenom} {self.nom}".strip()

    def get_short_name(self):
        """Retourne le prénom de l'utilisateur"""
        return self.prenom or self.email



# Model pour enregistre les region 
class Region(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=30, unique=True)
    code_iso = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.libelle


# Model pour enregistre les Departement
class Departement(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=50)
    code_iso = models.CharField(max_length=30)
    region = models.ForeignKey(Region,on_delete=models.SET_NULL,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.libelle


# Model pour enregistres les commune
class Commune(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=50)
    code_iso = models.CharField(max_length=30)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.libelle


# Model pour enregistre les unité de mesure
class UniteMesure(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=30, unique=True)
    symbole = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.libelle

# Model pour enregistres les periode 
class Periode(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=255)
    annee = models.DateField(default=timezone.now) 
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.libelle} ({self.annee})"
    

# Model pour enregistre les bailleur qui sont des organisme de fiancement comme fonjip ...
class Bailleur(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    code_bailleur = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="bailleurs/logos/", blank=True, null=True)
    sigle = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.nom} ({self.code_bailleur})"



# Model pour enregistre nos Type d'indicateur
class TypeDindicateur(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.libelle
    
    
# Model pour nous permetre d'enregistre nos indicateur
class Indicateur(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    formule_calcul = models.CharField(max_length=255)  # Stocke la formule en texte simple
    type_indicateur = models.ForeignKey(TypeDindicateur, on_delete=models.SET_NULL, null=True, blank=True)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.libelle

# Ajoue du model programmes pour ajouter les programmes
class Programme(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=255, unique=True)
    bailleur = models.ForeignKey(Bailleur, on_delete=models.SET_NULL, null=True, blank=True)
    
    cout_programme = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.libelle
# Ce model vas permetre de lier un programme a un indicateur avec la possiblité d'un many to many
class ProgrammeIndicateur(models.Model):
    PERIODICITE_CHOICES = [
        ('journalier', 'Journalier'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
        ('trimestriel', 'Trimestriel'),
        ('semestriel', 'Semestriel'),
        ('annuel', 'Annuel'),
    ]
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    indicateur = models.ForeignKey('Indicateur', on_delete=models.CASCADE, null=False)
    programme = models.ForeignKey('Programme', on_delete=models.CASCADE, null=False)
    periodicite = models.CharField(max_length=20, choices=PERIODICITE_CHOICES, default='mensuel')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['programme', 'indicateur'], name='unique_programme_indicateur')
        ]

    def __str__(self):
        return f"{self.programme} - {self.indicateur}"
# Model pour enregistres les composante
class Composante(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=255, unique=True)
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.libelle

# Model pour enregistre les sous composante
class SousComposante(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=255, unique=True)
    composante = models.ForeignKey(Composante, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.libelle

# Model pour enregistre les projet
class Projet(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    libelle = models.CharField(max_length=255, unique=True)
    sigle = models.CharField(max_length=50, unique=True)
    date_entree_en_vigueur = models.DateField()
    date_demarrage_prevu = models.DateField()
    date_fin_prevu = models.DateField()
    cout_estime = models.DecimalField(max_digits=10, decimal_places=2)
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, blank=True)
    composante = models.ForeignKey(Composante, on_delete=models.SET_NULL, null=True, blank=True)
    sous_composante = models.ForeignKey(SousComposante, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.libelle
# Model pour enregistre les valeurs collecter
class Collecte(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    indicateur = models.ForeignKey('Indicateur', on_delete=models.CASCADE)
    valeur = models.FloatField(null=True, blank=True)
    valeur_prevu = models.FloatField(null=True, blank=True)
    date_collecte = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    periode_label = models.CharField(max_length=50, null=True, blank=True)
    periode = models.IntegerField(null=True, blank=True)    

    def __str__(self):
        return self.valeur

# Model pour configuirer un fiche de collecte 
class FicheCollecteConfiguration(models.Model):
    NIVEAU_CHOIX = [
        ('region', 'Région'),
        ('departement', 'Département'),
        ('commune', 'Commune'),
    ]
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOIX)
    libelle = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.libelle} - {self.get_niveau_display()}"

# Fiche de collecte pour les données a suivre
class FicheCollecteDonnee(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    configuration = models.ForeignKey(FicheCollecteConfiguration, on_delete=models.CASCADE, related_name='donnees')
    libelle = models.CharField(max_length=100)
    unite_mesure = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.libelle
    
# Les valeur collecté pour un fiche de collecte
class FicheCollecteValeur(models.Model):
    slug = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    donnee = models.ForeignKey(FicheCollecteDonnee, on_delete=models.CASCADE, related_name='valeurs')
    valeur = models.FloatField(null=True, blank=True)
    
    # Champs dynamiques selon le niveau de découpage
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, null=True, blank=True)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, blank=True)
    
    date_collecte = models.DateField(auto_now_add=True)
    periode = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.donnee.libelle} : {self.valeur}"