from django import forms

from .models import *


class AddSolution(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['homework_solution']

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateLesson(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['group', 'materials', 'number', 'name']

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
