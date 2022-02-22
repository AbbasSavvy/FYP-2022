# Generated by Django 3.0.7 on 2022-02-22 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_jd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='jd',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='placecomuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]