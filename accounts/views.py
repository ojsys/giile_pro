from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from .models import User

class SignUpView(View):
    template_name = 'accounts/signup.html'
    
    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Set to False if email verification is required
            user.save()
            
            # Send verification email (commented out for now)
            # self.send_verification_email(request, user)
            
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})
    
    def send_verification_email(self, request, user):
        """
        Send an email verification link to the user.
        """
        current_site = get_current_site(request)
        mail_subject = 'Activate your Giile Pro account'
        message = render_to_string('accounts/verification_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

class VerifyEmailView(View):
    """
    View to handle email verification.
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            user.email_verified = True
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified. You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Activation link is invalid or has expired.')
            return redirect('core:home')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:home')
    
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me', False)
        if not remember_me:
            # Session expires when the user closes their browser
            self.request.session.set_expiry(0)
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')

class ProfileView(LoginRequiredMixin, View):
    """
    View to display user profile.
    """
    template_name = 'accounts/profile.html'
    
    def get(self, request):
        return render(request, self.template_name, {'user': request.user})

class ProfileUpdateView(LoginRequiredMixin, View):
    """
    View to update user profile.
    """
    template_name = 'accounts/profile_update.html'
    
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})
