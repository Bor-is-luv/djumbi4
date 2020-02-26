from django.shortcuts import render
from .models import *
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CreateGroup, CreateCourse, CreateTeacher


def cabinet_view(request):
    context = {}
    template = 'cabinet/cabinet.html'

    # context['groups'] = Group.objects.get(teacher=request.user.id)
    return render(request, template, context)


class CreateGroupView(CreateView):
    model = Group
    template_name = 'create_group.html'
    form_class = CreateGroup
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.teacher = teacher
        self.object.save()
        return super().form_valid(form)


class CreateCourseView(CreateView):
    model = Course
    template_name = 'create_course.html'
    form_class = CreateCourse
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)


class CreateTeacherView(CreateView):
    model = Teacher
    template_name = 'create_teacher.html'
    form_class = CreateTeacher
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save()
        self.object.save()
        return super().form_valid(form)