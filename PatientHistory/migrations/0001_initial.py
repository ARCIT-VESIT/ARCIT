# Generated by Django 3.1 on 2020-12-01 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatientHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_status', models.CharField(max_length=50)),
                ('symtomps', models.CharField(max_length=1000)),
                ('disease', models.CharField(max_length=200)),
                ('affected_area', models.CharField(max_length=200)),
                ('timespan', models.CharField(max_length=100)),
                ('precription', models.CharField(max_length=1000)),
                ('course_duration', models.CharField(max_length=100)),
                ('follow_up', models.CharField(max_length=100, null=True)),
                ('referred_from', models.CharField(max_length=100, null=True)),
                ('referred_to', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]