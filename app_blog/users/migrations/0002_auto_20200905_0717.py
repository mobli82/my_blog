# Generated by Django 3.1 on 2020-09-05 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='img',
            new_name='profile_img',
        ),
    ]