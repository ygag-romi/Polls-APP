from django.contrib import admin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Details', {'fields': ('first_name', 'last_name',
                                         'date_of_birth',)}),
        (None, {'fields': ('nickname',)}),
        (None, {'fields': ('image',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active',
                                    'groups', 'user_permissions')}),
        ('Account important-dates', {'fields': ('last_login',
                                                'date_joined',)}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'date_of_birth', 'image_tag',
                    'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
