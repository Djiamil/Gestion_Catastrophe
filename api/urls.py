from django.urls import path
from api.views import *

urlpatterns = [
    # Debu des endPointe des fonction qui sont dans views
    path('login/', LoginView.as_view(), name='login'),
    # Fin des endpoint qui sont dans views
]

# Username superuser: Djiamil
# Email address: djiamil@gmail.com
# Password: Passer123!