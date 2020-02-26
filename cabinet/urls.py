from django.urls import path
from .views import cabinet_view, CreateGroupView, CreateCourseView, CreateTeacherView, \
    CreateLessonView


urlpatterns = [
    path('', cabinet_view, name='cabinet_page'),
    path('create_group/', CreateGroupView.as_view(), name='create_group_page'),
    path('create_course/', CreateCourseView.as_view(), name='create_course_page'),
    path('create_teacher/', CreateTeacherView.as_view(), name='create_teacher_page'),
    path('create_lesson/', CreateLessonView.as_view(), name='create_lesson_page'),
]