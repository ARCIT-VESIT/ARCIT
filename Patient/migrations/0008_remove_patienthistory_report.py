# Generated by Django 3.1.4 on 2020-12-12 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0007_auto_20201212_1212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patienthistory',
            name='report',
        ),
    ]