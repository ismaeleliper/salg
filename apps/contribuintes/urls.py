from django.urls import path
from . import views

app_name = 'contribuintes'

urlpatterns = [
    # path('criar_contribuinte/', views.create_contribuinte, name='criar_contribuinte'),
    path('criar_contribuinte/', views.CreateContribuinte.as_view(extra_context={'title': 'Criar Contribuinte',
                                                                                'title_bar': 'Novo Contribuinte'}),
         name='criar_contribuinte'),
    path('contribuinte/<int:pk>/', views.ContribuinteDetailView.as_view(extra_context={'title': 'Contribuinte',
                                                                                       'title_bar': 'Contribuinte',
                                                                                       'active_contribuintes': 'active'}),
         name='detalhes_contribuinte'),
    path('', views.ContribuinteListView.as_view(extra_context={'title': 'Contribuintes',
                                                               'title_bar': 'Contribuintes',
                                                               'active_contribuintes': 'active'}),
         name='contribuintes'),

    path('atualizar/<int:pk>', views.UpdateContribuinte.as_view(), name='atualizar_contribuinte'),
    path('del/<int:pk>', views.DeleteContribuinte.as_view(), name='delete_contribuinte'),
]
