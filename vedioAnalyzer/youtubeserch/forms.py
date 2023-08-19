from django import forms
from . models import *

class youtubeForm (forms.Form):
    
    text = forms.CharField(max_length = 100, label = "Enter your search :")
    
class SearchForm(forms.Form):
    youtubeLink = forms.CharField( required = False,  widget= forms.TextInput
                           (attrs={
                               'class': 'form-control',
                               'name': 'youtubeLink',
                               'placeholder':'Enter youtube link',
                               'required': 'false'
                            }))