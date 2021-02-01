from django.urls import path
from . import views

app_name = 'tesouraria'

urlpatterns = [

    path('criar_lancamento_oferta/', views.LancarOfertaView.as_view(), name='criar_lancamento_oferta'),
    # path('criar_lancamento_oferta/', views.create_lanc_oferta, name='criar_lancamento_oferta'),
    path('lancamento_oferta/<int:pk>', views.view_lancamento_oferta, name='lancamento_oferta'),
    path('lancamentos_oferta/', views.lancamentos_oferta, name='lancamentos_oferta'),

    path('criar_oferta/', views.create_oferta, name='criar_oferta'),
    path('oferta/<int:pk>', views.view_oferta, name='oferta'),
    path('ofertas/', views.ofertas, name='ofertas'),

    #path('contribuinte-name-search/', views.contribuinte_name_search, name='contribuinte-name-search'),

    path('criar_caixa/', views.create_caixa, name='criar_caixa'),
    path('caixa/<int:pk>', views.view_caixa, name='caixa'),
    path('editar_caixa/<int:pk>', views.update_caixa, name='editar_caixa'),
    path('deletar_caixa/<int:pk>', views.delete_caixa, name='deletar_caixa'),
    path('caixas/', views.caixas, name='caixas'),

    path('criar-entrada-manual/', views.create_entrada_no_caixa, name='criar-entrada-manual'),
    #path('criar_saida/', views.create_saida_no_caixa, name='criar_saida'),

    path('movimentacoes/<int:pk>', views.movimentacoes, name='movimentacoes'),
    path('lancamentos_oferta_caixa/<int:pk>', views.lancamentos_oferta_caixa,
         name='lancamentos_oferta_caixa'),

]