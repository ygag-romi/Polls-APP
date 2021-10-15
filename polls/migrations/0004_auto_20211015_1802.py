# Generated by Django 3.1 on 2021-10-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_question_open'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='open',
        ),
        migrations.AddField(
            model_name='question',
            name='closed',
            field=models.BooleanField(default=True, help_text='marks a poll as closed'),
        ),
    ]
