from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.core.mail import send_mail
from .lab2 import cipher

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
    class Meta:
        model = User
        fields = ('email', 'username', 'password')

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
            'ENTER YOU GMAIL',
            [f'{user.email}'],
            fail_silently=False,
        )
        if commit:
            user.save()
        return user
