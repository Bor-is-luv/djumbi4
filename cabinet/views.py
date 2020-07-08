from django.shortcuts import render, Http404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.detail import DetailView
from django.conf import settings

from .forms import *
from .models import *

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import Permission

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

import os

from PIL import Image

from django.shortcuts import redirect

# not a controller
try:
    User.objects.create_superuser(username='admin', email='mail@mail.ru', password='qwerty1234')
except:
    pass


# not a controller
def check_if_file_exitsts_and_delete(path: str) -> None:
    if os.path.exists(os.path.join(settings.MEDIA_ROOT, path)):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, path))
        except:
            pass

# not a controller
# change the size of the image to (300, 300)
def process_image(path: str) -> None:
    image = Image.open(os.path.join(settings.MEDIA_ROOT, path))
    image = image.resize((300, 300))
    image.save(os.path.join(settings.MEDIA_ROOT, path))

# not a controller
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

    def form_valid(self, form):
        if self.request.user.is_staff:
            return super().form_valid(form)
        else:
            raise PermissionDenied


class CreateTeacherView(CreateView, LoginRequiredMixin):

    response_data = {'status': 'ok'}
    model = Teacher
    template_name = 'cabinet/create_teacher.html'
    form_class = CreateTeacher
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        if self.request.user.is_staff:
            self.object = form.save(commit=False)
            user = self.object.user
            pupil = Pupil.objects.get(user=user)
            user.user_permissions.set(
                Permission.objects.filter(content_type_id__gte=7))
            user.save()
            delete_course = Permission.objects.get(codename='delete_course')
            add_course = Permission.objects.get(codename='add_course')
            delete_teacher = Permission.objects.get(codename='delete_teacher')
            add_teacher = Permission.objects.get(codename='add_teacher')
            user.user_permissions.remove(delete_course, add_course, 
                                         delete_teacher, add_teacher)
            user.save()
            pupil.delete()
            return super().form_valid(form)
        else:
            raise PermissionDenied


class CreateLessonView(PermissionRequiredMixin, CreateView, LoginRequiredMixin):
    permission_required = 'cabinet.add_lesson'
    model = Lesson
    template_name = 'cabinet/create_lesson.html'
    form_class = CreateLesson
    success_url = reverse_lazy('cabinet_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        teacher = Teacher.objects.get(user=self.request.user)
        self.object.teacher = teacher
        self.object.save()
        pupils = Pupil.objects.filter(group=self.object.group)
        self.object.pupils.set(pupils)
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

    context['lesson'] = lesson
    context['user_type'] = ctx['user_type']

    if ctx['user_type'] == 'pupil':
        context['homework'] = Solution.objects.filter(
            lesson=lesson, pupil_id=ctx['user'].id)
    elif ctx['user_type'] == 'teacher':
        context['homework'] = Solution.objects.filter(
            lesson=lesson)
        for solution in Solution.objects.filter(lesson=lesson):
            setattr(solution, 'seen_by_teacher', True)
            solution.save()
    if request.method == 'POST' and ctx['user_type'] == 'pupil':
        form = AddSolution(request.POST, request.FILES)
        if form.is_valid():
            pupil = Pupil.objects.get(id=ctx['user'].id)
            lesson = Lesson.objects.get(id=lesson_id)
            # it there already is a solution for this lesson for this pupil
            solutions = Solution.objects.filter(pupil=pupil, lesson=lesson)
            # delete all associated files here
            for solution in solutions:
                if os.path.exists(os.path.join(settings.MEDIA_ROOT, solution.homework_solution.name)):
                    os.remove(os.path.join(settings.MEDIA_ROOT,
                                           solution.homework_solution.name))
            # delete the solutions in the db
            solutions.delete()
            solution = Solution.objects.create(
                pupil=pupil, lesson=lesson, done=True, homework_solution=form.cleaned_data['homework_solution'])
        return redirect('cabinet_page')

    elif ctx['user_type'] == 'pupil':
        form = AddSolution()

    if ctx['user_type'] == 'pupil':
        context['form'] = form

    return render(request, 'cabinet/detail_lesson.html', context)


class DetailGroupView(DetailView, LoginRequiredMixin):
    model = Group
    template_name = 'cabinet/detail_group.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['group_teacher'] = Teacher.objects.get(pk=self.object.teacher_id)
        return context


class DetailTeacherView(DetailView, LoginRequiredMixin):
    model = Teacher
    template_name = 'cabinet/detail_teacher.html'


class DetailPupilView(DetailView, LoginRequiredMixin):
    model = Pupil
    template_name = 'cabinet/detail_pupil.html'


class UpdateGroupView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = 'cabinet.change_group'
    model = Group
    form_class = UpdateGroup
    template_name = 'cabinet/update_group.html'
    success_url = '/cabinet/'

    def form_valid(self, form):
        teacher = self.request.user.teacher
        if self.object.teacher != teacher:
            raise PermissionDenied
        else:
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UpdateGroupView, self).get_form_kwargs()
        kwargs['obj'] = self.object
        return kwargs


class UpdateCourseView(UpdateView, LoginRequiredMixin):
    model = Course
    form_class = UpdateCourse
    template_name = 'cabinet/update_course.html'
    success_url = '/cabinet/'

    def form_valid(self, form):
        if self.request.user.is_staff:
            return super().form_valid(form)
        else:
            raise PermissionDenied


class UpdateLessonView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = 'cabinet.change_lesson'
    model = Lesson
    form_class = UpdateLesson
    template_name = 'cabinet/update_lesson.html'
    success_url = '/cabinet/'


class UpdateSolutionView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = 'cabinet.change_solution'
    model = Solution
    form_class = UpdateSolution
    template_name = 'cabinet/update_lesson.html'
    success_url = '/cabinet/'


class UpdateUserView(UpdateView, LoginRequiredMixin):
    model = User
    template_name = 'cabinet/update_user.html'
    form_class = UpdateUser
    success_url = '/cabinet/'

    def form_valid(self, form):
        user = self.request.user
        if self.object != user:
            raise PermissionDenied
        else:
            return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UpdateUserView, self).get_form_kwargs()
        kwargs['obj'] = self.object
        kwargs['user'] = self.request.user
        return kwargs

@permission_required('cabinet.change_teacher')
@login_required
def update_teacher(request, pk):
    context = {}
    teacher = Teacher.objects.get(user_id=pk)
    user = teacher.user
    if request.method == 'POST':
        form = UpdateTeacher(request.POST, request.FILES)
        if form.is_valid():
            setattr(user, 'first_name', form.cleaned_data['first_name'])
            user.save()
            setattr(user, 'last_name', form.cleaned_data['last_name'])
            user.save()

            # delete the previous photo
            check_if_file_exitsts_and_delete(teacher.image.name)

            setattr(teacher, 'image', form.cleaned_data['image'])
            teacher.save()

            # change the size of the new photo
            try:
                process_image(form.cleaned_data['image'].name)
            except:
                pass

        return redirect('cabinet_page')
    else:
        form = form = UpdateTeacher(initial={
                             'first_name': teacher.user.first_name, 'last_name': teacher.user.last_name, 'image': teacher.image})
        context['form'] = form

        return render(request, 'cabinet/update_teacher.html', context)


class UpdatePupilView(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    permission_required = 'cabinet.change_pupil'
    model = Pupil
    form_class = UpdatePupil
    template_name = 'cabinet/update_pupil.html'
    success_url = '/cabinet/'

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


# AJAX
# course_name, user_id, keywords
def search_lesson_ajax(request):
    request_data = json.loads(request.body)
    response_data = {}
    response_data['lesson_name'] = []
    response_data['lesson_number'] = []
    response_data['lesson_id'] = []
    response_data['group'] = []

    # return all the lessons
    # TODO return the lessons only from the specific course
    try:
        user = Pupil.objects.get(user_id=request_data['user_id'])
        course = Course.objects.get(pk=request_data['course_id'])
        groups = Group.objects.filter(course_id=course.id)  # <--- CHECK IT!!!
        for group in groups:
            if user in group.pupils.all():
                lessons = Lesson.objects.filter(group_id=group.id)
                if (request_data['keywords']) is not '':
                    lessons = lessons.filter(
                        name__icontains=request_data['keywords'])
                for lesson in lessons:
                    response_data['lesson_name'].append(lesson.name)
                    response_data['lesson_number'].append(lesson.number)
                    response_data['lesson_id'].append(lesson.id)
    except:
        try:
            course = Course.objects.get(pk=request_data['course_id'])
            user = Teacher.objects.get(user_id=request_data['user_id'])
            groups = Group.objects.filter(
                teacher_id=user.id, course_id=course.id)
            for group in groups:
                lessons = Lesson.objects.filter(group_id=group.id)
                if (request_data['keywords']) is not '':
                    lessons = lessons.filter(
                        name__icontains=request_data['keywords'])
                for lesson in lessons:
                    response_data['lesson_name'].append(lesson.name)
                    response_data['lesson_number'].append(lesson.number)
                    response_data['lesson_id'].append(lesson.id)
                    response_data['group'].append(group.name)
                
        except:
            pass
        # find the user, then find the course, then finally find the group
        # and the lesson from that group

        # find the specific lesson
        # in SQLite non-ASCII characters are case-sensitive only

    content = json.dumps(response_data)
    response = HttpResponse(content, content_type='application/json')

    return response


def get_pupil_lessons(request, pupil_id, course_id):
    context = {}
    context['lessons'] = []
    pupil = Pupil.objects.get(pupil_id)
    course = Course.objects.get(course_id)
    groups = Group.objects.filter(course=course)
    for group in groups:
        if pupil in group.pupils:
            lessons = Lesson.objects.filter(group=group)
            context['lessons'].extend(lessons)

    # template = ???
    return render(request, template, context)


def get_pupils_not_in_group(request, group_id):
    context = {}
    context['pupils'] = []
    group = Group.objects.get(group_id)
    pupils_in_group = group.pupils
    pupils = Pupil.objects.all()
    for pupil in pupils:
        if pupil not in pupils_in_group:
            context['pupils'].append(pupil)

    # template = 'cabinet/add_pupil.html'
    return render(request, template, context)


def add_pupil_to_group(request, pupil_id, group_id):
    context = {}
    group = Group.objects.get(group_id)
    pupil = Pupil.objects.get(pupil_id)
    group.pupils.add(pupil)
    course = group.course
    course.pupils.add(pupil)

    # template = ???
    # context is empty now
    return render(request, template, context)


def download_solution(request, solution_id):
    solution = Solution.objects.get(id=solution_id)
    file_path = os.path.join(
        settings.MEDIA_ROOT, solution.homework_solution.name)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
        except:
            pass
    raise Http404


class ListCourseView(ListView):
    template_name = 'cabinet/view_courses.html'
    context_object_name = 'courses'
    model = Course

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['user_ctx'] = get_user_ctx(self.request)
        return context

class ListTeachersView(ListView):
    template_name = 'cabinet/view_teachers.html'
    context_object_name = 'teachers'
    model = Teacher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['user_ctx'] = get_user_ctx(self.request)
        return context

class ListGroupsView(ListView):
    template_name = 'cabinet/view_groups.html'
    context_object_name = 'groups'
    model = Group

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['user_ctx'] = get_user_ctx(self.request)
        return context


def view_solutions_by_ajax(request):
    request_data = json.loads(request.body)
    teacher_id = request_data['teacher_id']

    teacher = Teachers.objects.get(id=teacher_id)
    groups = teacher.group_set.all()
    lessons = []
    solutions = []

    for group in groups:
        for lesson in group.lesson_set.all():
            lessons.append(lesson)

    for lesson in lessons:
        for solution in lesson.solution_set.all():
            solutions.append(solution)

    result_pupils = []
    result_groups = []
    result_lessons = []
    for solution in solutions:
        if not solution.seen_by_teacher:
            result_pupils.append(solution.pupil.user.first_name + solution.pupil.user.last_name)
            lesson = solution.lesson
            result_lessons.append(lesson.name)
            result_groups.append(lesson.group.name)

    response_data['lesson_name'] = result_lessons
    response_data['group_name'] = result_groups
    response_data['pupil_name'] = result_pupils

    content = json.dumps(response_data)
    response = HttpResponse(content, content_type='application/json')

    return response