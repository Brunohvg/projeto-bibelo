from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("cotar/", views.cotar, name="cotar"),
    path("cotacoes/listar/", views.listar_cotacoes, name="listar_cotacoes"),
    path("cotacoes/visualizar/<str:identificador>/", views.cotacao, name="cotacao"),
    path("cotacoes/visualizar/gerar_os/<str:identificador>/", views.gerar_os, name="gerar_os")
]
