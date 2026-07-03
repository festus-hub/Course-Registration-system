from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

from .models import CustomUser
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


def landing_page(request):
    return render(request, 'landing.html')


def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            messages.success(request, f"If an account exists for {email}, instructions have been sent.")
            return redirect('login')
        messages.error(request, 'Please enter your email address.')

    return render(request, 'accounts/password_reset.html')

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
