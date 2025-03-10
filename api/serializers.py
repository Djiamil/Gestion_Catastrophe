from api.models import *
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['user_id'] = user.id
        data['email'] = user.email
        return data
    
# Le serializers du model role pour la gestion des role
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
# Le serializers principale de l'utilisateur retourner apres connexion
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    class Meta:
        model = User
        # exclude = ['password']
        fields = '__all__'
        
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # exclude = ['password']
        fields = '__all__'

# Serializer pour creer une region
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        
class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'
class CommuneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commune
        fields = '__all__'
        
class UniteMesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniteMesure
        fields = '__all__'

class PeriodeSerializer(serializers.ModelSerializer):
    annee = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%d-%m-%Y"])
    date_debut = serializers.SerializerMethodField()
    date_fin = serializers.SerializerMethodField()
    class Meta:
        model = Periode
        fields = '__all__'
    def get_date_debut(self, obj):
        return obj.date_debut.date() if obj.date_debut else None

    def get_date_fin(self, obj):
        return obj.date_fin.date() if obj.date_fin else None

class BailleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bailleur
        fields = '__all__'

class TypeDindicateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDindicateur
        fields = '__all__'

class IndicateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicateur
        fields = '__all__'
class ProgrammeSerializer(serializers.ModelSerializer):
    date_debut = serializers.SerializerMethodField()
    date_fin = serializers.SerializerMethodField()

    class Meta:
        model = Programme
        fields = '__all__'

    def get_date_debut(self, obj):
        return obj.date_debut.date() if obj.date_debut else None

    def get_date_fin(self, obj):
        return obj.date_fin.date() if obj.date_fin else None
class GetProgrammeSerializer(serializers.ModelSerializer):
    bailleur = BailleurSerializer()
    class Meta:
        model = Programme
        fields = '__all__'
class ConfiguirationIndicateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammeIndicateur
        fields = '__all__'