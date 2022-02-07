from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/', views.teacher, name='teacher'),
    path('student/', views.student, name='student'),
    path('login_page/', views.login_page, name='login_page'),
    path('login_teacher/', views.login_teacher, name='login_teacher'),
    path('login_student/', views.login_student, name='login_student'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('logout_page/', views.logout_page, name='logout_page')
]