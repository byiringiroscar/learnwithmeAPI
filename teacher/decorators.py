from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


def student_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_student == True and user.is_teacher == True:
            return view_func(request, *args, **kwargs)
        elif user.is_student:
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('login_student')

    return wrapper_func


def teacher_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = request.user
        if user.is_student and user.is_teacher:
            return view_func(request, *args, **kwargs)
        elif user.is_teacher:
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return redirect('logout_page')

    return wrapper_func


def student_only_api(view_func):
    def wrapper_funct(request, *args, **kwargs):
        user = request.user
        if user.is_student == True and user.is_teacher == True:
            return view_func(request, *args, **kwargs)
        elif user.is_student:
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            return HttpResponse('NOT ALLOWED')

    return wrapper_funct
