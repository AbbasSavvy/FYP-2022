# Generated by Django 3.2.12 on 2022-03-13 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qna', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ques_ans',
            name='skill_id',
            field=models.TextField(),
        ),
    ]
