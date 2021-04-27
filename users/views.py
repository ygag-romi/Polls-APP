from django.views.generic.edit import FormMixin, CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.views import View
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, get_user_model
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()


class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def send_user_verification_mail(self, request, user):
        current_site = get_current_site(request)
        subject = 'Activate your polls account'
        message = render_to_string('users/account_activation_email.html', {
            'users': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            self.send_user_verification_mail(request, user)

            messages.success(request,
                             'Please confirm your email to complete '
                             'registration.')

            return redirect('users:login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            user.is_active = True
            user.save()
            # login(request, user) for the user to be logged in after verifying
            messages.success(request, 'Your account has been verified')
            return redirect('users:login')

        else:
            messages.warning(request,
                             "Confirmation link invalid, please verify "
                             "that the link hasn't been used before.")
            return redirect('polls:index')


class ChangePasswordView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Your password has been changed!"
    success_url = reverse_lazy('polls:index')



