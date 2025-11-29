from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False  # User is inactive until email is verified
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email


class EmailVerificationForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        help_text='Enter your email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        })
    )
    otp = forms.CharField(
        max_length=6,
        help_text='Enter the 6-digit code sent to your email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456'
        })
    )


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        help_text='Enter your registered email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'youremail@example.com'
        })
    )


class PasswordResetVerifyForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'youremail@example.com'
        })
    )
    otp = forms.CharField(
        max_length=6,
        help_text='Enter the 6-digit code sent to your email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456'
        })
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")

        return cleaned_data