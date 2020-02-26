from django.urls import path
from .views import UserLoginView, UserRegisterView, UserLogoutView  # *


urlpatterns = [
    path('', UserLoginView.as_view(), name='login_page'),
    path('register', UserRegisterView.as_view(), name='registration_page'),
    path('logout', UserLogoutView.as_view(), name='logout_page'),
]