# Generated by Django 3.2.12 on 2022-03-13 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mcq_Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mcq_file', models.FileField(upload_to='mcq')),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
    ]
