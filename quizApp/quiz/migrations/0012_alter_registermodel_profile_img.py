# Generated by Django 5.0 on 2023-12-25 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_quizmodel_neg_marks_quizmodel_pos_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='profile_img',
            field=models.ImageField(blank=True, default='media/profile_images/userprofile.png', null=True, upload_to='profile_images'),
        ),
    ]
