# Generated by Django 3.2 on 2021-08-11 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patient', '0019_auto_20210713_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='state',
            field=models.CharField(default=1, max_length=254),
            preserve_default=False,
        ),
    ]
