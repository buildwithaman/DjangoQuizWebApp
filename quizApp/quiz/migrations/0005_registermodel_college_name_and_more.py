# Generated by Django 5.0 on 2023-12-20 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_alter_registermodel_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='registermodel',
            name='college_name',
            field=models.CharField(blank=True, default='Not Available', max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='registermodel',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='registermodel',
            name='profile_img',
            field=models.ImageField(blank=True, default='static/images/userprofile.png', null=True, upload_to='profile_images'),
        ),
    ]
