# Generated by Django 3.2 on 2021-08-16 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0016_alter_doctor_active_hours'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activehour',
            old_name='userid',
            new_name='doctor_id',
        ),
    ]