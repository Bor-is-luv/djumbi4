from django.shortcuts import render
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreateGroup, CreateCourse, CreateTeacher, CreateLesson
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required()
def cabinet_view(request):
    context = {}
    template = 'cabinet/cabinet.html'
    # teacher = Teacher.objects.get(user=request.user)
    # print(teacher)
    # courses = Course.objects.filter(teachers=teacher)
    # groups = Group.objects.filter(teacher=teacher)
    # lessons = Lesson.objects.filter(teacher=teacher)
    # context['groups'] = groups
    # context['lessons'] = lessons
    # context['courses'] = courses
    return render(request, template, context)


class CreateGroupView(CreateView, LoginRequiredMixin):
    model = Group
    template_name = 'cabinet/create_group.html'
    form_class = CreateGroup
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.teacher = teacher
        self.object.save()
        return super().form_valid(form)


class CreateCourseView(CreateView, LoginRequiredMixin):
    model = Course
    template_name = 'cabinet/create_course.html'
    form_class = CreateCourse
    success_url = reverse_lazy('cabinet_page')


class CreateTeacherView(CreateView, LoginRequiredMixin):
    model = Teacher
    template_name = 'cabinet/create_teacher.html'
    form_class = CreateTeacher
    success_url = reverse_lazy('cabinet_page')


class CreateLessonView(CreateView, LoginRequiredMixin):
    model = Teacher
    template_name = 'cabinet/create_lesson.html'
    form_class = CreateLesson
    success_url = reverse_lazy('cabinet_page')



