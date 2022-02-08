from .models import User
from .models import TeacherProfile, Course_week, Register_course, course_day
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        TeacherProfile.objects.create(user=instance)
        print("profile created")


@receiver(post_save, sender=Register_course)
def create_weeks(sender, instance, created, **kwargs):
    if created:
        week_loop = instance.duration_week
        for week in range(week_loop):
            Course_week.objects.create(course=instance, weeks=f'week {week + 1}')
            print("week created")


@receiver(post_save, sender=Course_week)
def create_days(sender, instance, created, **kwargs):
    if created:
        day_loop = instance.course.duration_day
        for day in range(day_loop):
            course_day.objects.create(week=instance)
            print("day created")

