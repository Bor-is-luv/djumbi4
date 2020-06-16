from django.urls import path
from .views import *


urlpatterns = [
    path('', cabinet_view, name='cabinet_page'),
    path('create_group/', CreateGroupView.as_view(), name='create_group_page'),
    path('create_course/', CreateCourseView.as_view(), name='create_course_page'),
    path('create_teacher/', CreateTeacherView.as_view(), name='create_teacher_page'),
    path('create_lesson/', CreateLessonView.as_view(), name='create_lesson_page'),
    path('detail_course/<int:pk>/', DetailCourseView.as_view(), name='detail_course_page'),
    path('detail_group/<int:pk>/', DetailGroupView.as_view(), name='detail_group_page'),
    path('detail_lesson/<int:pk>/', DetailLessonView.as_view(), name='detail_lesson_page'),
    path('detail_teacher/<int:pk>/', DetailTeacherView.as_view(), name='detail_teacher_page'),
    path('detail_pupil/<int:pk>/', DetailPupilView.as_view(), name='detail_pupil_page'),
    path('update_course/<int:pk>/', UpdateCourseView.as_view(), name='update_course_page'),
    path('update_group/<int:pk>/', UpdateGroupView.as_view(), name='update_group_page'),
    path('update_lesson/<int:pk>/', UpdateLessonView.as_view(), name='update_lesson_page'),
    path('update_teacher/<int:pk>/', UpdateTeacherView.as_view(), name='update_teacher_page'),
    path('update_pupil/<int:pk>/', UpdatePupilView.as_view(), name='update_pupil_page'),
    path('get_lesson_ajax/', fetch_lesson_ajax, name='fetch_lesson_ajax_url'),
]