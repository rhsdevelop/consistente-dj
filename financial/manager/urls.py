import django.contrib.auth.views
from django.urls import path

from . import views 

app_name = 'manager'
urlpatterns = [
    path('', views.index, name='index'),
    path('cliente/add/', views.add_cliente, name='add_cliente'),
    path('cliente/list/', views.list_cliente, name='list_cliente'),
    path('cliente/<int:cliente_id>/edit/', views.edit_cliente, name='edit_cliente'),
    path('clienteuser/add/', views.add_clienteuser, name='add_clienteuser'),
    path('clienteuser/list/', views.list_clienteuser, name='list_clienteuser'),
    path('clienteuser/<int:usuario_id>/edit/', views.edit_clienteuser, name='edit_clienteuser'),
    path('banco/add/', views.add_banco, name='add_banco'),
    path('banco/list/', views.list_banco, name='list_banco'),
    path('banco/<int:banco_id>/edit/', views.edit_banco, name='edit_banco'),
    path('categoria/add/', views.add_categoria, name='add_categoria'),
    path('categoria/list/', views.list_categoria, name='list_categoria'),
    path('categoria/<int:categoria_id>/edit/', views.edit_categoria, name='edit_categoria'),
    path('parceiro/add/', views.add_parceiro, name='add_parceiro'),
    path('parceiro/list/', views.list_parceiro, name='list_parceiro'),
    path('parceiro/<int:parceiro_id>/edit/', views.edit_parceiro, name='edit_parceiro'),
    path('receber/add/', views.add_receber, name='add_receber'),
    path('receber/list/', views.list_receber, name='list_receber'),
    path('receber/<int:diario_id>/edit/', views.edit_receber, name='edit_receber'),
    path('pagar/add/', views.add_pagar, name='add_pagar'),
    path('pagar/list/', views.list_pagar, name='list_pagar'),
    path('pagar/<int:diario_id>/edit/', views.edit_pagar, name='edit_pagar'),
    path('pagar/<int:diario_id>/delete/', views.delete_pagar, name='delette_pagar'),
    path('transferir/add/', views.add_transferir, name='add_transferir'),
    path('transferir/list/', views.list_transferir, name='list_transferir'),
    path('transferir/<int:diario_id>/edit/', views.edit_transferir, name='edit_transferir'),
    path('cartoes/list/', views.list_cartoes, name='list_cartoes'),
    path('cartoes/<int:diario_id>/edit/', views.edit_cartoes, name='edit_cartoes'),
    path('relatorio/caixa/', views.fluxo_caixa, name='fluxo_caixa'),
    path('relatorio/caixa/<int:diario_id>/pagar/', views.pagar_fluxo_caixa, name='pagar_fluxo_caixa'),
]
