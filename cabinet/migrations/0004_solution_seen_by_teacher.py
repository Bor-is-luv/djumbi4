# Generated by Django 3.0.3 on 2020-07-08 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet', '0003_auto_20200705_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='seen_by_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
