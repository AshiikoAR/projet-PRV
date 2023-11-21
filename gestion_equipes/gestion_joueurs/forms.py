from django import forms
from .models import Equipe, Joueur

class EquipeForm(forms.ModelForm):
    class Meta:
        model = Equipe
        fields = ['nom_equipe']  # Les champs que vous souhaitez afficher dans le formulaire

class JoueurForm(forms.ModelForm):
    equipe = forms.ModelChoiceField(queryset=Equipe.objects.all(), label='Sélectionnez une équipe', empty_label=None)

    def __init__(self, *args, **kwargs):
        super(JoueurForm, self).__init__(*args, **kwargs)
        self.fields['equipe'].choices = [(equipe.id, equipe.nom_equipe) for equipe in Equipe.objects.all()]

    class Meta:
        model = Joueur
        fields = ['nom_joueur', 'equipe']