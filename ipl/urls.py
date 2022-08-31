import imp
from django.contrib import admin
from django.urls import path
from ipl import views

urlpatterns = [
    path('', views.home),
    path('extraruns', views.extra_runs),
    path('ecobowlers', views.eco_bowlers),
    path('playedvswon', views.played_vs_won),
]
