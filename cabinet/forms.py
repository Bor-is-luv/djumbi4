from django.forms import ModelForm

from .models import Group, Course, Teacher, Lesson


class CreateGroup(ModelForm):
    class Meta:
        model = Group
        fields = ['course', 'name', 'time', 'day']

    def __init__(self, *args, **kwargs):
        qs_course = Course.objects.all()
        print(kwargs)
        if 'user' in kwargs and kwargs['user'] is not None:
            user = kwargs.pop('user')
            teacher = Teacher.objects.filter(user=user).first()
            print(teacher)
            qs_course = Course.objects.filter(teachers=teacher)
            print(qs_course)

        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = qs_course

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateCourse(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'hours']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateTeacher(ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateLesson(ModelForm):
    class Meta:
        model = Lesson
        fields = ['group', 'materials', 'number', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      #СДЕЛАТЬ ЗДЕСЬ ТАК ЖЕ КАК И В ГРУППАХ
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
