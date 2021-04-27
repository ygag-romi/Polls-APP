from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'first_name', 'last_name',)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        query = User.objects.filter(email=email)
        if query.exists():
            raise forms.ValidationError("Email is taken")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)


class CustomPasswordChangeForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Email does not exist")
        elif not User.objects.get(email=email).is_active:
            raise ValidationError("This account has not been verified")

        return email


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError("This account has not been verified!")
