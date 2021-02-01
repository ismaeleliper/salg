from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('registro/', RegisterView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]