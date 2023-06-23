from django import forms
from .models import Post

from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'marka',
            'model',
            'agirlik',
            'kategori',
            'image',
        ]

class KiralaForm(forms.ModelForm):
    kiralayan = forms.CharField(max_length=100, disabled=True)

    class Meta:
        model = Post
        fields = [
            'kiralayan',
            'baslama_tarih',
            'bitis_tarih',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.kiralayan:
            self.fields['kiralayan'].initial = self.instance.user.get_full_name()

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.kiralayan = self.instance.kiralayan
        instance.baslama_tarih = self.cleaned_data['baslama_tarih']
        instance.bitis_tarih = self.cleaned_data['bitis_tarih']

        if commit:
            instance.save()

        return instance