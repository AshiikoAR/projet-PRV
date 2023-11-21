from django.urls import path
from . import views

urlpatterns = [
    path('liste_joueurs_par_equipe/', views.liste_joueurs_par_equipe, name='liste_joueurs_par_equipe'),
    path('modifier_joueur_equipe/<int:joueur_id>/', views.modifier_joueur_equipe, name='modifier_joueur_equipe'),
    path('shuffle_joueurs/', views.shuffle_joueurs, name='shuffle_joueurs'),
    path('ajout_equipe/', views.ajout_equipe, name='ajout_equipe'),
    path('ajout_joueur/', views.ajout_joueur, name='ajout_joueur'),
    path('supprimer_joueur/<int:joueur_id>/', views.supprimer_joueur, name='supprimer_joueur'),
    path('supprimer_equipe/<int:equipe_id>/', views.supprimer_equipe, name='supprimer_equipe'),
]