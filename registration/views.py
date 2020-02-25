from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.views.generic import CreateView
from .forms import AuthUserForm, RegisterUserForm
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'registration/index.html')


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('create_group_page')

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
    template_name = 'registration/register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login_page')
    # success_msg = 'Пользователь успешно создан'


class UserLogoutView(LogoutView):
    next_page = 'register_page'
