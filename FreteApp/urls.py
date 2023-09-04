from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("cotacoes/", views.cotacao, name="cotacao"),
    path("listar_cotacoes/", views.listar_cotacoes, name='listar_cotacoes')
]
