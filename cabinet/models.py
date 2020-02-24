from django.db import models
from django.contrib.auth.models import User


class Pupil(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    image = models.ImageField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=15)


class Course(models.Model):
    pupils = models.ManyToManyField(Pupil)
    teachers = models.ManyToManyField(Teacher)

    name = models.CharField(max_length=20)
    hours = models.IntegerField(blank=True, null=True, default=0)
    active = models.BooleanField(default=False)


class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель', blank=True, null=True)
    pupils = models.ManyToManyField(Pupil, verbose_name='ученики')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length=20)
    time = models.DateField(blank=True, null=True)
    day = models.CharField(blank=True, null=True, max_length=12)
    active = models.BooleanField(default=False)


class Lesson(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.DO_NOTHING)
    pupils = models.ManyToManyField(Pupil)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

    materials = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=30)
    homework_task = models.TextField(blank=True, null=True)
    homework_solution = models.FileField(blank=True, null=True)
