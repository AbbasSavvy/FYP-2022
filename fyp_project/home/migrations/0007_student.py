# Generated by Django 3.2.12 on 2022-03-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20220222_1353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=50)),
                ('sap_id', models.IntegerField(unique=True)),
                ('program', models.CharField(max_length=50)),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField(max_length=1)),
                ('division', models.IntegerField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=3)),
                ('placement', models.BooleanField()),
            ],
        ),
    ]
