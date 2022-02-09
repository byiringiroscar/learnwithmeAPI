from teacher.models import Register_course
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class RegisterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register_course
        fields = ['course_title', 'course_subtitle', 'course_description', 'course_level',
                  'course_category', 'course_image', 'duration_week', 'duration_day']

    def validate(self, attrs):
        number_week = 12
        number_day = 7
        duration_week = attrs.get('duration_week', '')
        duration_day = attrs.get('duration_day', '')
        if duration_week > number_week:
            raise AuthenticationFailed("number of week are too many than 12")
        if duration_day > number_day:
            raise AuthenticationFailed("number of day are too many than 7")
        return super().validate(attrs)
