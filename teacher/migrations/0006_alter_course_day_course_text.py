# Generated by Django 4.0.1 on 2022-02-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_rename_duration_register_course_duration_week_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_day',
            name='course_text',
            field=models.TextField(max_length=250),
        ),
    ]