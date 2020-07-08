from django.db import models
from django.contrib.auth.models import User

def get_first_name(self):
    return self.first_name + ' ' + self.last_name

User.add_to_class("__str__", get_first_name)


class Pupil(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user.__str__() }'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    image = models.ImageField('Фотография', blank=True, null=True)
    info = models.TextField('Информация', blank=True, null=True)
    phone_number = models.CharField('Телефонный номер', blank=True, null=True, max_length=15)

    def __str__(self):
        return f'{self.user.__str__() }'

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Course(models.Model):
    pupils = models.ManyToManyField(Pupil, blank=True, null=True, verbose_name='Ученики')
    teachers = models.ManyToManyField(Teacher, blank=True, null=True, verbose_name='Учителя')

    name = models.CharField('Название', max_length=50)
    hours = models.IntegerField('Количество часов', blank=True, null=True, default=0)
    active = models.BooleanField(default=True)
    info = models.TextField('Информация', blank=True, null=True, max_length=400)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        constraints = [
            models.CheckConstraint(check=models.Q(hours__gte=0), name='hours_gte_0'),
        ]


class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING,
                                verbose_name='Учитель', blank=True, null=True)
    pupils = models.ManyToManyField(Pupil, verbose_name='Ученики')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='Курс')

    name = models.CharField('Название', max_length=20)
    time = models.CharField('Время проведения занятия', max_length=20, blank=True, null=True)
    day = models.CharField('День занятия', blank=True, null=True, max_length=12)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.course} {self.time} {self.day}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING, verbose_name='Учитель')
    pupils = models.ManyToManyField(Pupil, verbose_name='Ученики')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, verbose_name='Группа')

    materials = models.TextField('материалы к уроку', blank=True, null=True)
    number = models.IntegerField('Номер урока', blank=True, null=True)
    name = models.CharField('Название урока', max_length=30)
    homework_task = models.TextField('Домашнее задание', blank=True, null=True)

    def __str__(self):
        return f'{self.group} {self.number}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Solution(models.Model):
    homework_solution = models.FileField('Решение', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, verbose_name='Урок')
    pupil = models.ForeignKey(Pupil, on_delete=models.DO_NOTHING, verbose_name='Ученик')
    done = models.BooleanField(default=False)

    seen_by_teacher = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.lesson} {self.pupil}'