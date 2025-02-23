from django.urls import path
from api.views import *

urlpatterns = [
    # Debu des endPointe des fonction qui sont dans views 
    path('login/', LoginView.as_view(), name='login'),
    path('role_create/', AddRole.as_view(), name='create_role'),
    path('user_create/', AddUser.as_view(), name='create_user'),
    # Fin des endpoint qui sont dans views
]

# Username superuser: Djiamil
# Email address: djiamil@gmail.com
# Password: Passer123!