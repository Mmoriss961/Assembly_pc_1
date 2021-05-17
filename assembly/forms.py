import email
from wsgiref import validate
from django.db import models
from  django import forms
from  django.core.exceptions import ValidationError
from  django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from  django.contrib.auth.models import User
from django.core.validators import validate_email, EmailValidator
from email_validator import validate_email, EmailNotValidError
from assembly.models import Feedback


class UserRegisterForm (UserCreationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Логин",'type':"text"}))
    first_name = forms.CharField(label='Имя',widget=forms.TextInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Имя",'type':"text"}))
    last_name = forms.CharField(label='Фамилия',widget=forms.TextInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Фамилия",'type':"text"}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Email",'type':"text"}))
    password1 = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Пароль",'type':"password"}))
    password2 = forms.CharField(label='Подтверждение пароля',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Подтвердите пароль",'type':"password"}))


    class Meta:
        model = User
        fields =('username','first_name','last_name','email','password1','password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:

            return email

        raise forms.ValidationError('Этот Email уже используется')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            match = User.objects.get(username=username)
        except User.DoesNotExist:

            return username

        raise forms.ValidationError('Этот Логин уже используется')

class UserLoginForm (AuthenticationForm):
    username = forms.CharField(label='Логин',widget=forms.TextInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Логин",'type':"text"}))
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Пароль",'type':"password"}))

class FeedbackForm(forms.ModelForm):
    from_email  = forms.EmailField(label='Укажите Email',widget=forms.TextInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Email",'type':"text"}))
    subject  = forms.CharField(label='Тема',widget=forms.TextInput(attrs={'class':'form-control','autocomplete':"off",'placeholder':"Тема",'type':"text"}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', 'autocomplete': "off", 'placeholder': "Сообщение", 'type': "text",'rows':5}))

    class Meta:
        model = Feedback
        fields = ['from_email','subject','message']