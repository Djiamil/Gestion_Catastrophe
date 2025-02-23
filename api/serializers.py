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
