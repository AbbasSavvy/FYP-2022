# Generated by Django 3.2.12 on 2022-03-17 10:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_delete_mcq_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='skills',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='placement',
            field=models.CharField(default='Unplaced', max_length=8),
        ),
    ]