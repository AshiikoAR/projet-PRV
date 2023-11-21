from django.db import models

class Equipe(models.Model):
    nom_equipe = models.CharField(max_length=100)

class Joueur(models.Model):
    nom_joueur = models.CharField(max_length=100)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)

class Transfert(models.Model):
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)