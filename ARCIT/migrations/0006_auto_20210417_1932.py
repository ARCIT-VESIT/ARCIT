# Generated by Django 2.2.6 on 2021-04-17 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ARCIT', '0005_auto_20201210_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, verbose_name='first name'),
        ),
    ]
