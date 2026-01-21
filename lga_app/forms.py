from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from lga_app.models import Article, Category, Comment

class UpdateUserForm(UserChangeForm):
	#email = forms.EmailField(label="",	 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
	username = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilisateur'}))
	#last_name = forms.CharField(label="", max_length=100,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
	class Meta:
		model = User
		fields = ('username', 'first_name')
	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['email'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['placeholder'] = 'User Name'
		self.fields['email'].label = ''
		self.fields['email'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'


class ArticleForm(forms.ModelForm):
    users = User.objects.all()
    categories = Category.objects.all()

    title = forms.CharField(label="Titre",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Titre'}),
                              required=True)

    summary = forms.CharField(label="Résumé",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Résumé'}),
                              required=True)

    content = forms.CharField(label="Contenu",
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu'}),
                              required=True)

    author = forms.ModelChoiceField(users)

    category = forms.ModelChoiceField(categories)
    image = forms.ImageField(required=False)

    class Meta:
        model = Article
        fields = ('title', 'summary', 'content', 'category',  'author', 'image')


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='text',
                            widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'text'}),
                            required=False)

    class Meta:
        model = Comment
        fields = ('text',)
