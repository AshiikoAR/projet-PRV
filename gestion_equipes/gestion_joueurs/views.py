import random
from random import shuffle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Joueur, Equipe, Transfert
from .forms import EquipeForm, JoueurForm

def est_admin(user):
    return user.is_authenticated and user.username == 'PRV' and user.check_password('1234')  # Vérifie l'identifiant et le mot de passe

def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.username == 'PRV' and user.check_password('1234'):
            login(request, user)
            return redirect('accueil_admin')  # Rediriger vers la page d'accueil de l'administrateur après la connexion
        else:
            # Gérer les erreurs d'identification
            pass  # Vous pouvez ajouter ici la logique pour gérer les erreurs de connexion

    return render(request, 'login_admin.html')  # Afficher le formulaire de connexion pour l'administrateur

def liste_joueurs_par_equipe(request):
    equipes = Equipe.objects.all()
    return render(request, 'liste_joueurs_par_equipe.html', {'equipes': equipes})

@user_passes_test(est_admin)
def ajout_equipe(request):
    if request.method == 'POST':
        form = EquipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_joueurs_par_equipe')  # Rediriger vers la liste des équipes après l'ajout
    else:
        form = EquipeForm()
    return render(request, 'ajout_equipe.html', {'form': form})

@user_passes_test(est_admin)
def ajout_joueur(request):
    if request.method == 'POST':
        form = JoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_joueurs_par_equipe')  # Rediriger vers la liste des joueurs après l'ajout
    else:
        form = JoueurForm()
    return render(request, 'ajout_joueur.html', {'form': form})

@user_passes_test(est_admin)
def modifier_joueur_equipe(request, joueur_id):
    joueur = Joueur.objects.get(pk=joueur_id)
    
    if request.method == 'POST':
        equipe_id = request.POST['equipe']
        equipe = Equipe.objects.get(pk=equipe_id)
        joueur.equipe = equipe
        joueur.save()
        
        return redirect('liste_joueurs_par_equipe')  # Redirection vers la liste des joueurs par équipe
    
    return render(request, 'modifier_joueur_equipe.html', {'joueur': joueur, 'equipes': Equipe.objects.all()})

@user_passes_test(est_admin)
def supprimer_joueur(request, joueur_id):
    joueur = get_object_or_404(Joueur, pk=joueur_id)
    if request.method == 'POST':
        joueur.delete()
        return redirect('liste_joueurs_par_equipe')  # Redirection vers la liste des joueurs après la suppression
    return render(request, 'confirm_suppression_joueur.html', {'joueur': joueur})

@user_passes_test(est_admin)
def supprimer_equipe(request, equipe_id):
    equipe = get_object_or_404(Equipe, pk=equipe_id)
    if request.method == 'POST':
        # Supprimer tous les joueurs associés à cette équipe
        equipe.joueur_set.all().delete()
        # Supprimer l'équipe elle-même
        equipe.delete()
        return redirect('liste_joueurs_par_equipe')  # Redirection vers la liste des joueurs par équipe après la suppression
    return render(request, 'confirm_suppression_equipe.html', {'equipe': equipe})

@user_passes_test(est_admin)
def shuffle_joueurs(request):
    equipes = list(Equipe.objects.all())
    joueurs = list(Joueur.objects.all())

    random.shuffle(joueurs)

    # Supprime toutes les associations existantes entre les joueurs et les équipes
    Transfert.objects.all().delete()

    # Associe chaque joueur à une équipe de manière aléatoire
    for i, joueur in enumerate(joueurs):
        equipe = equipes[i % len(equipes)]
        Transfert.objects.create(joueur=joueur, equipe=equipe)

    return redirect('liste_joueurs_par_equipe')

