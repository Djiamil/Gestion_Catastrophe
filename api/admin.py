from django.contrib import admin

# Register your models here.

from api.models import *

class UserAdmin(admin.ModelAdmin):

    search_fields = ("email",) 

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Region)
admin.site.register(Departement)
admin.site.register(Commune)
admin.site.register(UniteMesure)
admin.site.register(Periode)
admin.site.register(Bailleur)
admin.site.register(TypeDindicateur)
admin.site.register(Indicateur)
admin.site.register(Collecte)
admin.site.register(FicheCollecteConfiguration)
admin.site.register(FicheCollecteDonnee)
admin.site.register(FicheCollecteValeur)
