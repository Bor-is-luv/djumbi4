from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import AuthUserForm, RegisterUserForm
from django.contrib.auth import authenticate, login

from .lab2 import uncipher_str
from cabinet.models import Pupil

def confirm(request, key):
    username = uncipher_str(key)
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    pupil = Pupil()
    pupil.user = user
    pupil.save()
    template = 'registration/confirm_page.html'
    return render(request, template)

class UserLoginView(LoginView):
    template_name = 'registration/login_page.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('cabinet_page')

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class UserRegisterView(CreateView):
    model = User
    template_name = 'registration/registration_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login_page')
    # success_msg = 'Пользователь успешно создан'


class UserLogoutView(LogoutView):
    next_page = 'registration_page'
