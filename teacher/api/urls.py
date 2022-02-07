from django.urls import path
from .views import TeacherRegistrationView, StudentRegistrationView, VerifyEmail, LoginStudentAPIView, LoginTeacherAPIView

urlpatterns = [
    path('registerteacher', TeacherRegistrationView.as_view(), name='registerteacher'),
    path('registerstudent', StudentRegistrationView.as_view(), name='registerstudent'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('loginstudent/', LoginStudentAPIView.as_view(), name='login-student'),
    path('loginteacher/', LoginTeacherAPIView.as_view(), name='login-teacher'),
]