from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from core.models import *



#####################     creating signup form     ######################

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#####################     creating update profile form     ######################

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email')

#####################     creating update profile picture form     ######################

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']





class ArticleForm(forms.ModelForm):
    # subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # message = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # college = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # picture = forms.ImageField(widget=forms.ImageInput(attrs={'class':'form-control'}))
    # tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model   = Article
        fields  = ['subject', 'message','college', 'image', 'tags']





class AnnouncementCreateForm(forms.ModelForm):
    class Meta:
        model   = Announcement
        fields  = ['title', 'content']