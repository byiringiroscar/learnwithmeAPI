from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from teacher.models import StudentProfile, TeacherProfile
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import TeacherProfile, Course_week, Register_course, course_day

User = get_user_model()

# Remove Group Model from admin we are not using it
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['first_name', 'last_name', 'email', 'is_student', 'is_teacher', 'is_verified', 'admin']
    list_filter = ['admin']
    fieldsets = (
        (None, {'fields': ('first_name', 'email', 'is_student', 'is_teacher', 'is_verified', 'password')}),
        ('Personal info', {'fields': ('last_name',)}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password', 'password_2')}
         ),
    )
    search_fields = ['email']
    ordering = ['-id']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(Course_week)
admin.site.register(Register_course)
admin.site.register(course_day)
# admin.site.register(TeacherProfile)
# admin.site.register(StudentProfile)
