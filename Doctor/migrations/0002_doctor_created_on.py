# Generated by Django 2.2.6 on 2021-04-17 14:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]