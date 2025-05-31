from django import forms

class DorkForm(forms.Form):
    keyword = forms.CharField(
        max_length=200,
        required=False,
        label="Mot-clé",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le mot-clé'})
    )
   
    filetype = forms.CharField(
        max_length=50,
        required=False,
        label="Type de fichier (facultatif)",
        widget=forms.TextInput(attrs={'placeholder': 'ex: pdf'})
    )
    intitle = forms.CharField(
        max_length=200,
        required=False,
        label="Recherche dans le titre (facultatif)",
        widget=forms.TextInput(attrs={'placeholder': 'ex: admin'})
    )
    inurl = forms.CharField(
        max_length=200,
        required=False,
        label="Recherche dans l'URL (facultatif)",
        widget=forms.TextInput(attrs={'placeholder': 'ex: login'})
    )
    exclude = forms.CharField(
        max_length=200,
        required=False,
        label="Exclusion de termes (facultatif)",
        widget=forms.TextInput(attrs={'placeholder': 'ex: -demo'})
    )
