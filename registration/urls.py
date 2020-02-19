from django.urls import path
from .views import UserLoginView, UserRegisterView, index, UserLogoutView  # *


urlpatterns = [
    path('', index),
    path('login', UserLoginView.as_view(), name='login_page'),
    path('register', UserRegisterView.as_view(), name='register_page'),
    path('logout', UserLogoutView.as_view(), name='logout_page'),
]