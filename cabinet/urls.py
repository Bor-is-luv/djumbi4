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
    path('detail_lesson/<int:lesson_id>/', detail_lesson_view, name='detail_lesson_page'),
    path('detail_teacher/<int:pk>/', DetailTeacherView.as_view(), name='detail_teacher_page'),
    path('detail_pupil/<int:pk>/', DetailPupilView.as_view(), name='detail_pupil_page'),
    path('update_course/<int:pk>/', UpdateCourseView.as_view(), name='update_course_page'),
    path('update_group/<int:pk>/', UpdateGroupView.as_view(), name='update_group_page'),
    path('update_lesson/<int:pk>/', UpdateLessonView.as_view(), name='update_lesson_page'),
    path('update_teacher/<int:pk>/', update_teacher, name='update_teacher_page'),
    path('update_pupil/<int:pk>/', UpdatePupilView.as_view(), name='update_pupil_page'),
    path('update_user/<int:pk>/', UpdateUserView.as_view(), name='update_user_page'),
    path('fetch_lesson_ajax/', fetch_lesson_ajax, name='fetch_lesson_ajax_url'),
    path('search_lesson_ajax/', search_lesson_ajax, name='search_lesson_ajax_url'),
    path('get_pupil_lessons/<int:pupil>/<int:course>', get_pupil_lessons, name='get_pupil_lessons_url'),
    path('get_pupils_not_in_group/<int:group_id>', get_pupil_lessons, name='get_pupil_lessons_url'),
    path('add_pupil_to_group/<int:pupil_id>/<int:group_id>', get_pupil_lessons, name='get_pupil_lessons_url'),
    path('download_solution/<int:solution_id>', download_solution, name='download_solution_url'),
    path('list_courses/', ListCourseView.as_view(), name='list_courses_url'),
    path('list_teachers/', ListTeachersView.as_view(), name='list_teachers_url'),
    path('list_groups/', ListGroupsView.as_view(), name='list_groups_url'),
    path('alert_teacher/', view_solutions_by_ajax, name='view_solutions_by_ajax_url'),
]