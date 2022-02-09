from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from course.serializers import RegisterCourseSerializer
from teacher.models import Register_course
from course.permissions import IsOwner
from rest_framework import permissions


# Create your views here.

class RegisterCourseAPIView(ListCreateAPIView):
    serializer_class = RegisterCourseSerializer
    queryset = Register_course.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(course_owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(course_owner=self.request.user)


class DetailCourseAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = RegisterCourseSerializer
    queryset = Register_course.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(course_owner=self.request.user)
