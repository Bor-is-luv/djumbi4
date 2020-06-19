from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView

from .forms import *
from .models import *

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Permission

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def get_user_ctx(request):
    user = request.user
    context = {}
    try:
        pupil = Pupil.objects.get(user=user)
        context['user'] = pupil
        context['courses'] = Course.objects.filter(pupils=pupil)
        context['groups'] = Group.objects.filter(pupils=pupil)
        context['lessons'] = Lesson.objects.filter(pupils=pupil)
        context['user_type'] = 'pupil'
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        try:
            teacher = Teacher.objects.get(user=user)
            context['user'] = teacher
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


class CreateGroupView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = 'cabinet.add_group'
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


class CreateCourseView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = 'cabinet.add_course'
    model = Course
    template_name = 'cabinet/create_course.html'
    form_class = CreateCourse
    success_url = reverse_lazy('cabinet_page')

    #def form_valid(self, form):
    #    if self.request.user.is_staff:
    #        return super().form_valid(form)
    #    else:
    #       raise PermissionDenied


class CreateTeacherView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    
    response_data = {'status': 'ok'}
    #pupil = Pupil.objects.filter(pk=request.GET.get('user_id'))

    permission_required = 'cabinet.add_teacher'
    model = Teacher
    template_name = 'cabinet/create_teacher.html'
    form_class = CreateTeacher
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        if self.request.user.is_staff:
            self.object = form.save(commit=False)
            user = self.object.user
            pupil = Pupil.objects.get(user=user)
            user.user_permissions.set(Permission.objects.filter(content_type_id__gte=25))
            user.save()
            delete_course = Permission.objects.get(codename='delete_course')
            add_course = Permission.objects.get(codename='add_course')
            change_course = Permission.objects.get(codename='change_course')
            delete_teacher = Permission.objects.get(codename='delete_teacher')
            add_teacher = Permission.objects.get(codename='add_teacher')
            change_teacher = Permission.objects.get(codename='change_teacher')
            user.user_permissions.remove(delete_course, add_course, change_course,
                                         delete_teacher, add_teacher, 
                                         change_teacher)
            user.save()
            pupil.delete()
            return super().form_valid(form)
        else:
            raise PermissionDenied


class CreateLessonView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = 'cabinet.add_lesson'
    model = Teacher
    template_name = 'cabinet/create_lesson.html'
    form_class = CreateLesson
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.teacher = teacher
        pupils = Pupil.objects.filter(group=self.object.group)
        self.objects.pupils = pupils
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreateLessonView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DetailCourseView(DetailView, LoginRequiredMixin):
    model = Course
    template_name = 'cabinet/detail_course.html'


def detail_lesson_view(request, lesson_id):
    ctx = get_user_ctx(request)
    context = {}
    lesson = Lesson.objects.get(id=lesson_id)
    if ctx['user_type'] == 'pupil':
        context['homework'] = Solution.objects.filter(lesson=lesson, pupil=ctx['pupil'])
    elif ctx['user_type'] == 'teacher':
        context['homework'] = Solution.objects.filter(lesson=lesson, teacher=ctx['teacher'])

    if request.method == 'POST' and ctx['user_type'] == 'pupil':
        form = AddSolution(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
    elif ctx['user_type'] == 'pupil':
        form = AddSolution()

    context['form'] = form
    return render(request, 'cabinet/detail_pupil.html', context)


class DetailGroupView(DetailView, LoginRequiredMixin):
    model = Group
    template_name = 'cabinet/detail_group.html'


class DetailTeacherView(DetailView, LoginRequiredMixin):
    model = Teacher
    template_name = 'cabinet/detail_teacher.html'


class DetailPupilView(DetailView, LoginRequiredMixin):
    model = Pupil
    template_name = 'cabinet/detail_pupil.html'


class UpdateGroupView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = 'cabinet.change_update'
    model = Group
    template_name = 'cabinet/update_group.html'


class UpdateCourseView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = 'cabinet.change_course'
    model = Course
    template_name = 'cabinet/update_course.html'

class UpdateLessonView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = 'cabinet.change_lesson'
    model = Lesson
    template_name = 'cabinet/update_lesson.html'

class UpdateTeacherView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = 'cabinet.change_teacher'
    model = Teacher
    template_name = 'cabinet/update_teacher.html'

    #def form_valid(self, form):
    #    if self.request.user.is_staff:
    #        return super().form_valid(form)
    #    else:
    #        raise PermissionDenied

class UpdatePupilView(PermissionRequiredMixin, DetailView, LoginRequiredMixin):
    permission_required = 'cabinet.change_pupil'
    model = Pupil
    template_name = 'cabinet/update_pupil.html'


# AJAX

# lesson_id, course_id, user_id
def fetch_lesson_ajax(request):
    response_data = {'status': 'ok'}

    # get the lesson by its id
    lesson = Lesson.objects.get(id=request.GET.get('lesson_id'))

    # make a json with a response data 
    response_data['name'] = lesson.name
    response_data['number'] = lesson.number
    response_data['materials'] = lesson.materials
    response_data['homework_task'] = lesson.homework_task

    # convert it into json format
    content = json.dumps(response_data)
    # make the response itself
    response = HttpResponse(content, content_type='application/json')

    return response

# 
# course_name, user_id, keywords
def search_lesson_ajax(request):
    request_data = json.loads(request.body)

    response_data = {}
    response_data['lesson_name'] = []
    response_data['lesson_number'] = [] 
    response_data['lesson_id'] = []

    # return all the lessons
    # TODO return the lessons only from the specific course
    if request_data['keywords'] is None:
        lessons_to_find = Lesson.objects.all()
        for lesson in lessons_to_find:
            response_data['lesson_name'].append(lesson.name)
            response_data['lesson_number'].append(lesson.number)
            response_data['lesson_id'].append(lesson.id)
    else:
        try:
            user = Pupil.objects.get(pk=request_data['user_id'])
        except:
            try:
                user = Teacher.objects.get(pk=request_data['user_id'])
            except: 
                print('yo')
        # find the user, then find the course, then finally find the group
        # and the lesson from that group

        # find the specific lesson
        # in SQLite non-ASCII characters are case-sensitive only
        # sad T-T
        lessons_to_find = Lesson.objects.filter(name__icontains=request_data['keywords'])
        for lesson in lessons_to_find.all():
            response_data['lesson_name'].append(lesson.name)
            response_data['lesson_number'].append(lesson.number)
            response_data['lesson_id'].append(lesson.id)

    content = json.dumps(response_data)
    response = HttpResponse(content, content_type='application/json')

    return response

def get_pupil_lessons(request, pupil_id, course_id):
    context = {}
    context['lessons'] = []
    pupil = Pupil.objects.get(pupil_id)
    course = Course.objects.get(course_id)
    groups = course.group_set.all()
    for group in groups:
        if pupil in group.pupils:
            lessons = Lesson.objects.filter(group=group)
            context['lessons'].append(lessons)


    template = ???
    return render(request, template, context)

    