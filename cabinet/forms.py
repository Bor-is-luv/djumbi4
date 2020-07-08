from django import forms

from .models import *

from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied


class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        if 'obj' in kwargs and kwargs['obj'] is not None:
            obj = kwargs['obj']
            kwargs.pop('obj')

        if 'user' in kwargs and kwargs['user'] is not None:
            user = kwargs['user']
            kwargs.pop('user')

        if user != obj:
            raise PermissionDenied

        super().__init__(*args, **kwargs)


class UpdateGroup(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ('teacher', 'course')

    def __init__(self, *args, **kwargs):
        if 'obj' in kwargs and kwargs['obj'] is not None:
            group = kwargs['obj']
            course = group.course
            qs_pupils = course.pupils.all()
            kwargs.pop('obj') 
         
        super().__init__(*args, **kwargs)
        self.fields['pupils'].queryset = qs_pupils

class UpdateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        qs_pupils = Pupil.objects.all()
        super().__init__(*args, **kwargs)
        self.fields['pupils'].queryset = qs_pupils

class UpdateLesson(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'

class UpdateTeacher(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    image = forms.ImageField()

class UpdatePupil(forms.ModelForm):
    class Meta:
        model = Pupil
        fields = '__all__'

class UpdateSolution(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['homework_solution']

class AddSolution(forms.Form):
    homework_solution = forms.FileField(label="Домашняя работа")

class CreateGroup(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['course', 'name', 'time', 'day']

    def __init__(self, *args, **kwargs):
        qs_course = Course.objects.all()
        if 'user' in kwargs and kwargs['user'] is not None:
            user = kwargs.pop('user')
            teacher = Teacher.objects.filter(user=user).first()
            qs_course = Course.objects.filter(teachers=teacher)

        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = qs_course

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'hours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateTeacher(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
#
    def __init__(self, *args, **kwargs):
        qs_users = User.objects.all()
        qs_teachers = Teacher.objects.all()
        for teacher in qs_teachers:
            qs_users = qs_users.exclude(pk=teacher.user_id)

        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = qs_users
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateLesson(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['group', 'materials', 'number', 'name', 'homework_task']

    def __init__(self, *args, **kwargs):
        qs_groups = Group.objects.all()
        if 'user' in kwargs and kwargs['user'] is not None:
            user = kwargs.pop('user')
            teacher = Teacher.objects.filter(user=user).first()
            qs_groups = Group.objects.filter(teacher=teacher)

        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = qs_groups
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean_number(self):
        number = self.cleaned_data['number']

        if number < 0:
            raise ValidationError('Номер урока не может быть отрицательным')
        else:
            group = self.cleaned_data['group']
            lessons = Lesson.objects.filter(group=group)
            numbers = [lesson.number for lesson in lessons]
            if number in numbers:
                raise ValidationError('Урок с таким номером уже есть')
            
        return number
