from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from teacher.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status


class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        email = self.validated_data['email']
        if User.objects.filter(email=email, is_teacher=False, is_student=False):
            User.objects.filter(email=email).update(is_teacher=True)
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
        )
        email = self.validated_data['email']
        if User.objects.filter(email=email, is_teacher=True):
            raise serializers.ValidationError("user exist with this email")
        # if User.objects.filter(email=email, is_teacher=False, is_student=False):
        #     User.objects.filter(email=email).update(is_teacher=True)
        #     breakpoint()

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.is_teacher = True
        user.save()
        return user

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, max_length=250)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone_number=self.validated_data['phone_number'],
        )
        user_exist = User.objects.filter(email=self.validated_data['email'])
        # user_teacher_exist = User.objects.get(email=self.validated_data['email'], is_teacher=True)
        # if user_teacher_exist:
        #     update = User.objects.filter(email=self.validated_data['email']).update(is_student=True)
        #     data = {'status': 'user with email updated with role of teacher'}
        #     return Response(data=data, status=status.HTTP_201_CREATED)
        if user_exist:
            raise serializers.ValidationError({'email': 'email with this user exist'})
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match'})
        user.set_password(password)
        user.is_student = True
        user.save()
        return user

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginStudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=68, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials , try again')
        # if not user.is_student:
        #     raise AuthenticationFailed('You are not student you need to register as student')
        if not user.is_active:
            raise AuthenticationFailed("Account is disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        if user.is_teacher and user.is_student == False:
            raise AuthenticationFailed("User is teacher not student")
        if not user.is_student and user.is_teacher:
            raise AuthenticationFailed("User don;t have a status")
        if user and user.is_student == True:
            return {
                'email': user.email,
                'first_name': user.first_name,
                'tokens': user.tokens  # this is from models function tokens
            }
        if user.is_teacher and user.is_student:
            return {
                'email': user.email,
                'first_name': user.first_name,
                'tokens': user.tokens  # this is from models function tokens
            }

        return super().validate(attrs)


class LoginTeacherSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    first_name = serializers.CharField(max_length=68, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials , try again')
        if user.is_student == False and user.is_teacher == False:
            raise AuthenticationFailed("User not have status contact administrator")
        if not user.is_teacher:
            raise AuthenticationFailed('You are not Teacher you need to register as Teacher')
        if not user.is_active:
            raise AuthenticationFailed("Account is disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        if user.is_teacher:
            return {
                'email': user.email,
                'first_name': user.first_name,
                'tokens': user.tokens  # this is from models function tokens
            }
        if user.is_teacher and user.is_student:
            return {
                'email': user.email,
                'first_name': user.first_name,
                'tokens': user.tokens  # this is from models function tokens
            }

        return super().validate(attrs)
