# Generated by Django 4.0.1 on 2022-02-08 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_register_course_course_week'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register_course',
            old_name='duration',
            new_name='duration_week',
        ),
        migrations.AddField(
            model_name='register_course',
            name='duration_day',
            field=models.IntegerField(default=3),
        ),
        migrations.CreateModel(
            name='course_day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_link', models.URLField(max_length=100)),
                ('course_video', models.ImageField(upload_to='images/')),
                ('course_text', models.CharField(max_length=250)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.course_week')),
            ],
        ),
    ]