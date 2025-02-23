import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from safedelete.models import SafeDeleteModel


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