from django.db import models  
from django.forms import fields  
from .models import Image  
from django import forms 


class ImageForm(forms.Form):
    """Form for the image model"""
    class Meta:
        models = Image
        fields = '__all__'