import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .serializers import TeacherRegistrationSerializer, StudentRegistrationSerializer, EmailVerificationSerializer, \
    LoginStudentSerializer, LoginTeacherSerializer, RequestPasswordEmailSerializer, SetNewPasswordSerializer
from rest_framework import generics, status, views
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utilis import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


class TeacherRegistrationView(generics.GenericAPIView):
    serializer_class = TeacherRegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'hi ' + user.first_name + ' Use the link below to verify your email \n' + absurl

        data = {
            'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'
        }
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentRegistrationView(generics.GenericAPIView):
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        user_student = request.data
        serializer = self.serializer_class(data=user_student)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absoluteurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'hi ' + user.first_name + ' Use the link below to verify your email \n' + absoluteurl

        data = {
            'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'
        }
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginStudentAPIView(generics.GenericAPIView):
    serializer_class = LoginStudentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginTeacherAPIView(generics.GenericAPIView):
    serializer_class = LoginTeacherSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordEmailSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=data)
        email = request.data['email']
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://' + current_site + relativeLink
            email_body = 'hello, \n use this link to reset password\n' + absurl
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your password'}
            Util.send_email(data)
        return Response({'success': 'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credentials valid', 'uidb64': uidb64, 'token': token},
                            status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
