from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("cotacoes/", views.cotacao, name="cotacao"),
]
