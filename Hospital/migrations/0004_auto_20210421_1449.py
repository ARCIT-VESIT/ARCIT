# Generated by Django 3.2 on 2021-04-21 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0003_alter_hospital_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='created_on',
        ),
        migrations.AlterField(
            model_name='hospital',
            name='registeration_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='website',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
