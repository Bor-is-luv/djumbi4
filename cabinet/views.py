from django.shortcuts import render
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreateGroup, CreateCourse, CreateTeacher, CreateLesson


def cabinet_view(request):
    context = {}
    template = 'cabinet/cabinet.html'

    # context['groups'] = Group.objects.get(teacher=request.user.id)
    return render(request, template, context)


class CreateGroupView(CreateView):
    model = Group
    template_name = 'cabinet/create_group.html'
    form_class = CreateGroup
    success_url = reverse_lazy('cabinet_page')


class CreateCourseView(CreateView):
    model = Course
    template_name = 'cabinet/create_course.html'
    form_class = CreateCourse
    success_url = reverse_lazy('cabinet_page')


class CreateTeacherView(CreateView):
    model = Teacher
    template_name = 'cabinet/create_teacher.html'
    form_class = CreateTeacher
    success_url = reverse_lazy('cabinet_page')


class CreateLessonView(CreateView):
    model = Teacher
    template_name = 'cabinet/create_lesson.html'
    form_class = CreateLesson
    success_url = reverse_lazy('cabinet_page')



