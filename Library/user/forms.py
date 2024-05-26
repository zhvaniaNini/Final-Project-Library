from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Full Name', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    personal_number = forms.IntegerField(label='Personal Number', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label='Birth Date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'birth_date', 'password1', 'password2']