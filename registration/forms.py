from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.core.mail import send_mail
from .lab2 import cipher

from django.core.exceptions import ValidationError

import re


class RecoverAccountForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(label='name')
    surname = forms.CharField(label='surname')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        super().clean()
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        surname = self.cleaned_data['surname']
        if not User.objects.filter(email=email, name=name, surname=surname).exists():
            raise ValidationError('User not exists')



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='old password')
    new_password = forms.CharField(label='new password')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        if self.user.password != old_password:
            raise ValidationError("Old password not correct, try again")
        if old_password == new_password:
            raise ValidationError("New password cannot be equal to the old password")



class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(label='username')

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        cipher_username = cipher(username)
        message = f'localhost:8000/confirm/{cipher_username}'
        user.is_active = False
        send_mail(
            'Subject here',
            message,
            'zverkii5@gmail.com',
            [f'{user.email}'],
            fail_silently=False,
        )
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username must be unique')

        if not re.fullmatch(r'^[a-zA-Z0-9]+$', username):
            raise ValidationError('Only eng letters and numbers')

        return username
