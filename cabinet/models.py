from django.db import models
from django.contrib.auth.models import User


class Pupil(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    image = models.ImageField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=15)

    def __str__(self):
        return f'{self.user.username }'

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class Course(models.Model):
    pupils = models.ManyToManyField(Pupil, blank=True, null=True)
    teachers = models.ManyToManyField(Teacher, blank=True, null=True)

    name = models.CharField(max_length=50)
    hours = models.IntegerField(blank=True, null=True, default=0)
    active = models.BooleanField(default=True)
    info = models.TextField(blank=True, null=True, max_length=400)

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
    pupils = models.ManyToManyField(Pupil, verbose_name='ученики')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=20)
    time = models.CharField(max_length=20, blank=True, null=True)
    day = models.CharField(blank=True, null=True, max_length=12)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.course} {self.time} {self.day}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    pupils = models.ManyToManyField(Pupil)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

    materials = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    homework_task = models.TextField(blank=True, null=True)
    homework_solution = models.FileField(blank=True, null=True)

    def __str__(self):
        return f'{self.group} {self.number}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
