# Generated by Django 2.2.6 on 2021-04-17 14:49

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0012_auto_20210417_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='patienthistory',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_by',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
