from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from .models import CustomUser, PasswordResetToken
from students.models import Student


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if self.cleaned_data.get('role') == 'admin':
            user.is_staff = True
        if commit:
            user.save()
        return user


class SetNewPasswordForm(forms.Form):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2


def landing_page(request):
    return render(request, 'landing.html')


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                
                # Create a password reset token
                reset_token = PasswordResetToken.objects.create(
                    user=user,
                    expires_at=timezone.now() + timedelta(hours=24)
                )
                
                # Build reset link (adjust URL based on your domain)
                reset_link = request.build_absolute_uri(
                    f'/password-reset-confirm/{reset_token.token}/'
                )
                
                # Send email
                subject = 'Password Reset Request'
                message = f"""
Hello {user.first_name or user.username},

You have requested to reset your password. Click the link below to set a new password:

{reset_link}

This link will expire in 24 hours.

If you did not request this password reset, please ignore this email.

Best regards,
Course Registration System
"""
                send_mail(
                    subject,
                    message,
                    'noreply@courseregistration.com',
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'Password reset instructions have been sent to {email}')
                return redirect('login')
            except CustomUser.DoesNotExist:
                # Don't reveal if email exists or not (security best practice)
                messages.success(request, 'If an account exists for this email, you will receive password reset instructions.')
                return redirect('login')
        else:
            messages.error(request, 'Please enter your email address.')

    return render(request, 'accounts/password_reset.html')


def password_reset_confirm_view(request, token):
    """Handle password reset confirmation and new password setting"""
    reset_token = get_object_or_404(PasswordResetToken, token=token)
    
    # Check if token is valid
    if not reset_token.is_valid():
        messages.error(request, 'This password reset link has expired or is invalid.')
        return redirect('password_reset')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            # Update password
            user = reset_token.user
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            messages.success(request, 'Your password has been reset successfully. You can now login.')
            return redirect('login')
    else:
        form = SetNewPasswordForm()
    
    return render(request, 'accounts/password_reset_confirm.html', {'form': form, 'token': token})


# Register View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('role') == 'student':
                Student.objects.create(
                    user=user,
                    student_id=f'STU-{user.id:04d}',
                )
            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


# Login View
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('dashboard')

        messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('landing')
