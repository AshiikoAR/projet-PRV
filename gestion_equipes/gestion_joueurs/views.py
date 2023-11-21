import random
from random import shuffle
from django.shortcuts import render, redirect, get_object_or_404
from .models import Joueur, Equipe, Transfert
from .forms import EquipeForm, JoueurForm

def ajout_equipe(request):
    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_joueurs_par_equipe')  # Rediriger vers la liste des équipes après l'ajout
    else:
        form = EquipeForm()
    return render(request, 'ajout_equipe.html', {'form': form})

def ajout_joueur(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_joueurs_par_equipe')  # Rediriger vers la liste des joueurs après l'ajout
    else:
        form = JoueurForm()
    return render(request, 'ajout_joueur.html', {'form': form})

def liste_joueurs_par_equipe(request):
    equipes = Equipe.objects.all()
    return render(request, 'liste_joueurs_par_equipe.html', {'equipes': equipes})

def modifier_joueur_equipe(request, joueur_id):
    joueur = Joueur.objects.get(pk=joueur_id)
    
    if request.method == 'POST':
        equipe_id = request.POST['equipe']
        equipe = Equipe.objects.get(pk=equipe_id)
        joueur.equipe = equipe
        joueur.save()
        
        return redirect('liste_joueurs_par_equipe')  # Redirection vers la liste des joueurs par équipe
    
    return render(request, 'modifier_joueur_equipe.html', {'joueur': joueur, 'equipes': Equipe.objects.all()})

def supprimer_joueur(request, joueur_id):
    joueur = get_object_or_404(Joueur, pk=joueur_id)
    if request.method == 'POST':
        joueur.delete()
        return redirect('liste_joueurs_par_equipe')  # Redirection vers la liste des joueurs après la suppression
    return render(request, 'confirm_suppression_joueur.html', {'joueur': joueur})

def supprimer_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, pk=equipe_id)
    if request.method == 'POST':
        # Supprimer tous les joueurs associés à cette équipe
        equipe.joueur_set.all().delete()
        # Supprimer l'équipe elle-même
        equipe.delete()
        return redirect('liste_joueurs_par_equipe')  # Redirection vers la liste des joueurs par équipe après la suppression
    return render(request, 'confirm_suppression_equipe.html', {'equipe': equipe})


def shuffle_joueurs(request):
    equipes = list(Equipe.objects.all()) # Récupère toutes les équipes existantes
    joueurs = list(Joueur.objects.all()) # Récupère tous les utilisateurs existants

    random.shuffle(joueurs) # Mélange aléatoirement la liste des utilisateurs

    Transfert.objects.all().delete() # Réinitialise les associations utilisateur-équipe existantes

    for i, joueur in enumerate(joueurs):  # Modifier ici pour utiliser la variable 'joueur'
        equipe = equipes[i % len(equipes)]
        Transfert.objects.create(joueur=joueur, equipe=equipe)  # Utilisation de la variable 'joueur'

    return redirect('liste_joueurs_par_equipe')