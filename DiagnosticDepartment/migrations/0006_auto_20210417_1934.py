# Generated by Django 2.2.6 on 2021-04-17 14:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiagnosticDepartment', '0005_diagnosticdepartmentreport_create_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diagnosticdepartmentreport',
            name='create_on',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='created_on'),
        ),
    ]