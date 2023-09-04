from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("cotar/", views.cotar, name="cotar"),
    path("listar_cotacoes/", views.listar_cotacoes, name='listar_cotacoes'),
    path("cotacao/<str>id", views.cotacao, name="cotacao")
]
