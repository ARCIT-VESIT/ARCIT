# Generated by Django 3.2 on 2021-04-23 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0005_remove_doctor_created_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='last_name',
        ),
    ]