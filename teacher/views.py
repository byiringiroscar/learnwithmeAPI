from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model

User = get_user_model()
from .decorators import student_only, teacher_only


# Create your views here.

def home(request):
    return render(request, 'home.html')


def teacher(request):
    form = UserRegistrationForm()
    email = request.POST.get('email')
    user = User.objects.filter(email=email, is_student=True)
    if user:
        update_user = User.objects.filter(email=email, is_student=True).update(is_teacher=True)
        print("update_user", update_user)
        return redirect('login_teacher')
    elif request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            update = User.objects.filter(email=email).update(is_teacher=True)
            print("update user", update)
            print('name', email)
            return redirect('login_teacher')
    context = {
        'form': form
    }
    return render(request, 'teacher.html', context)


def student(request):
    student_form = UserRegistrationForm()
    email = request.POST.get('email')
    user = User.objects.filter(email=email, is_teacher=True)
    if user:
        update_user = User.objects.filter(email=email, is_teacher=True).update(is_student=True)
        print("update_user", update_user)
        return redirect('login_student')
    elif request.method == 'POST':
        student_form = UserRegistrationForm(request.POST, request.FILES)
        if student_form.is_valid():
            student_form.save()
            email = student_form.cleaned_data.get('email')
            update = User.objects.filter(email=email).update(is_student=True)
            print("update", update)
            return redirect('login_student')
    context = {
        'form': student_form
    }
    return render(request, 'student.html', context)


def login_page(request):
    return render(request, 'login_page.html')


def login_teacher(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_teacher == True:
            login(request, user)
            return redirect('teacher_dashboard')
        elif user is not None and user.is_student == True and user.is_teacher == True:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            messages.info(request, 'credential not match')
            return redirect('login_teacher')

    return render(request, 'teacher_login.html')


def login_student(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_student = authenticate(request, email=email, password=password)
        if user_student is not None and user_student.is_student == True:
            login(request, user_student)
            return redirect('student_dashboard')
        elif user_student is not None and user_student.is_student == True and user_student.is_teacher == True:
            login(request, user_student)
            return redirect('student_dashboard')
        else:
            messages.info(request, 'credential not match')
            return redirect('login_student')

    return render(request, 'student_login.html')


@teacher_only
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')


@student_only
def student_dashboard(request):
    return render(request, 'student_dashboard.html')


def logout_page(request):
    logout(request)
    return redirect('home')
