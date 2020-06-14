from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from .forms import CreateGroup, CreateCourse, CreateTeacher, CreateLesson
from .models import *

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_user_ctx(request):
    user = request.user
    context = {}
    context['user'] = ""
    try:
        pupil = Pupil.objects.get(user=user)
        context['user'] = pupil.user.username
        context['courses'] = Course.objects.filter(pupils=pupil)
        context['groups'] = Group.objects.filter(pupils=pupil)
        context['lessons'] = Lesson.objects.filter(pupils=pupil)
        context['user_type'] = 'pupil'
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        try:
            teacher = Teacher.objects.get(user=user)
            context['user'] = teacher.user.username
            context['courses'] = Course.objects.filter(teachers=teacher)
            context['groups'] = Group.objects.filter(teacher=teacher)
            context['lessons'] = Lesson.objects.filter(teacher=teacher)
            context['user_type'] = 'teacher'
        except ObjectDoesNotExist:
            context['user_type'] = 'admin'

    return context


@login_required()
def cabinet_view(request):
    template = 'cabinet/cabinet.html'
    context = get_user_ctx(request)

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

    def get_form_kwargs(self):
        kwargs = super(CreateGroupView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        pupil = Pupil.objects.get(user=self.object.user)
        pupil.delete()
        return super().form_valid(form)


class CreateLessonView(CreateView, LoginRequiredMixin):
    model = Teacher
    template_name = 'cabinet/create_lesson.html'
    form_class = CreateLesson
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.teacher = teacher
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateLessonView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DetailCourseView(DetailView, LoginRequiredMixin):
    model = Course
    template_name = 'cabinet/detail_course.html'


class DetailLessonView(DetailView, LoginRequiredMixin):
    model = Lesson
    template_name = 'cabinet/detail_lesson.html'


class DetailGroupView(DetailView, LoginRequiredMixin):
    model = Group
    template_name = 'cabinet/detail_group.html'
