from django.urls import path
from .views import TeacherRegistrationView, StudentRegistrationView, VerifyEmail, LoginStudentAPIView, \
    LoginTeacherAPIView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView

urlpatterns = [
    path('registerteacher', TeacherRegistrationView.as_view(), name='registerteacher'),
    path('registerstudent', StudentRegistrationView.as_view(), name='registerstudent'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('loginstudent/', LoginStudentAPIView.as_view(), name='login-student'),
    path('loginteacher/', LoginTeacherAPIView.as_view(), name='login-teacher'),
    path('password-reset-email', RequestPasswordResetEmail.as_view(), name='password-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete')

]
