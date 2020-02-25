from django.urls import path
from .views import cabinet_view, CreateGroupView, CreateCourseView


urlpatterns = [
    path('', cabinet_view, name='cabinet_page'),
    path('create_group/', CreateGroupView.as_view(), name='create_group_page'),
    path('create_course/', CreateCourseView.as_view(), name='create_course_page'),

]