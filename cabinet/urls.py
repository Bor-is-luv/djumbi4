from django.urls import path
from .views import cabinet_view, CreateGroupView


urlpatterns = [
    path('cabinet/', cabinet_view, name='cabinet_page'),
    path('create_group/', CreateGroupView.as_view(), name='create_group_page'),
]