from django.urls import path
from .views import *


urlpatterns = [
    path('', UserLoginView.as_view(), name='login_page'),
    path('register', UserRegisterView.as_view(), name='registration_page'),
    path('logout', UserLogoutView.as_view(), name='logout_page'),
    path('confirm/<str:key>', confirm, name='confirm_page'),
    path('recover_account/', recover_account, name='recover_account'),
    path('change_password/<int:pk>/', change_password, name='change_password'),
]