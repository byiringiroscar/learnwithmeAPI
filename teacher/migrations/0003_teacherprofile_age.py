# Generated by Django 4.0.1 on 2022-02-08 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_user_is_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacherprofile',
            name='age',
            field=models.DateField(blank=True, null=True),
        ),
    ]
