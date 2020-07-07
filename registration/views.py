from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User, Permission
from django.views.generic import CreateView

from django.contrib.auth import authenticate, login

from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import send_mail

from .forms import *
from .lab2 import uncipher_str
from cabinet.models import Pupil

from django.contrib.auth.decorators import login_required


def recover_account(request):
    if request.method == 'POST':
        form = RecoverAccountForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            user = User.objects.filter(name=name, surname=surname, email=email)
            password = User.objects.make_random_password()
            user.set_password(password)
            send_mail(
            'New password',
            password,
            'zverkii5@gmail.com',
            [f'{user.email}'],
            fail_silently=False)
            user.save()
        return redirect('login_page')
    else:
        form = RecoverAccountForm()

    return render(request, 'registration/recover_account.html', {'form':form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
    else:
        form = ChangePasswordForm()

    return render(request, 'registration/change_password.html', {'form':form})


def confirm(request, key):
    username = uncipher_str(key)
    user = User.objects.get(username=username)
    user.is_active = True
    user.user_permissions.clear()

    view_lesson = Permission.objects.get(codename='view_lesson')
    change_lesson = Permission.objects.get(codename='change_lesson')
    view_group = Permission.objects.get(name='Can view Группа')
    view_course = Permission.objects.get(codename='view_course')
    view_teacher = Permission.objects.get(codename='view_teacher')
    view_pupil = Permission.objects.get(codename='view_pupil')

    user.user_permissions.add(view_lesson, change_lesson, view_group, view_course, view_teacher, view_pupil)
    user.save()
    try:
        pupil = Pupil.objects.get(user=user)
    except ObjectDoesNotExist:
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
    next_page = 'login_page'
