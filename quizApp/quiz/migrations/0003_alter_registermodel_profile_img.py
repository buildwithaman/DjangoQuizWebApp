# Generated by Django 5.0 on 2023-12-19 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_registermodel_bio_alter_registermodel_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registermodel',
            name='profile_img',
            field=models.ImageField(blank=True, default='accounts/images/userprofile.png', null=True, upload_to='account/images'),
        ),
    ]