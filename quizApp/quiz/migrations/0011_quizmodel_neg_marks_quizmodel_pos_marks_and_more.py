# Generated by Django 5.0 on 2023-12-23 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_quizsubmissionmodel_userrankmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmodel',
            name='neg_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quizmodel',
            name='pos_marks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='quizmodel',
            name='quiz_duration',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
