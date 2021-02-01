from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('configurar-informacoes/', views.profile_edit, name='config'),
]