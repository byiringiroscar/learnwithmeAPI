from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError("Instructor must have an email address")
        if not first_name:
            raise ValueError("Instructor must have first_name")
        if not last_name:
            raise ValueError("Instructor must have an last_name ")
        if not phone_number:
            raise ValueError("Instructor must have phone_number")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, phone_number, password):
        if not email:
            raise ValueError("Instructor must have an email address")
        if not first_name:
            raise ValueError("Instructor must have first_name")
        if not last_name:
            raise ValueError("Instructor must have an last_name ")
        if not phone_number:
            raise ValueError("Instructor must have phone_number")
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password):

        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = PhoneNumberField(blank=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']  # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        return f'{self.first_name}--{self.last_name}'

    def get_short_name(self):
        return self.last_name

    def __str__(self):
        return f'{self.first_name}--{self.email}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class StudentProfile(models.Model):
    user = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
    # additional fields for students


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, related_name='teacher_profile', on_delete=models.CASCADE)

    # additional fields for teachers
    def __str__(self):
        return f'{self.user.first_name} -- {self.user.email}'
