# Generated by Django 5.0 on 2023-12-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0007_rename_category_categorymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizmodel',
            name='quiz_file',
            field=models.FileField(blank=True, null=True, upload_to='quiz_file'),
        ),
    ]
