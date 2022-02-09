from django.urls import path
from course.views import RegisterCourseAPIView, DetailCourseAPIView

urlpatterns = [
    path('', RegisterCourseAPIView.as_view(), name='create-course'),
    path('<int:id>', DetailCourseAPIView.as_view(), name='update-course')
]