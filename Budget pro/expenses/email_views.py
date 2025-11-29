from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .email_forms import CustomUserCreationForm, EmailVerificationForm, PasswordResetRequestForm, PasswordResetVerifyForm
import random
import string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
import os

# Only import twilio if credentials are available
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False


def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))


def send_otp_via_email(email, otp):
    """Send OTP via email"""
    try:
        subject = 'Budget Pro Verification Code'
        message = f'''
Hello,

Your verification code for Budget Pro is: {otp}

Please use this code to:
- Verify your account during signup
- Reset your password if you requested a password reset

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Budget Pro Team
        '''
        
        # Check if we're in development mode
        if settings.DEBUG and not os.environ.get('EMAIL_HOST_USER'):
            # In development without real email credentials, print to console
            print(f"=== EMAIL OTP ===")
            print(f"To: {email}")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print(f"==============")
            return True
        
        # Send actual email
        email_message = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        email_message.send()
        
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        # For development, print to console as fallback
        print(f"Email OTP for {email}: {otp}")
        return True


def send_otp_via_sms(phone_number, otp):
    """Send OTP via SMS using Twilio"""
    if not TWILIO_AVAILABLE or not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        # Fallback: Print to console for development
        print(f"SMS OTP for {phone_number}: {otp}")
        return True
    
    try:
        from twilio.rest import Client
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your Budget Pro verification code is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False


def signup_with_email_verification(request):
    """Sign up with email verification"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Use fixed OTP for development
            otp = "123456"
            
            # Store OTP in cache with 10-minute expiration
            cache.set(f'otp_signup_{user.email}', otp, 600)
            
            # For development, just notify that OTP is fixed
            print(f"FIXED OTP for {user.email}: {otp}")
            
            # Save user but keep inactive until verification
            user.save()
            messages.success(request, f'Account created! Use OTP {otp} to verify your email.')
            # Store email in session for verification
            request.session['verification_email'] = user.email
            return redirect('verify_email')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def verify_email(request):
    """Verify email with OTP"""
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            entered_otp = form.cleaned_data['otp']
            
            # Get stored OTP
            stored_otp = cache.get(f'otp_signup_{email}')
            
            if stored_otp and entered_otp == stored_otp:
                # OTP verified successfully
                try:
                    user = User.objects.get(email=email)
                    user.is_active = True  # Activate user
                    user.save()
                    messages.success(request, 'Email verified successfully!')
                    # Clear OTP from cache
                    cache.delete(f'otp_signup_{email}')
                    # Log in user
                    login(request, user)
                    # Clear session
                    if 'verification_email' in request.session:
                        del request.session['verification_email']
                    return redirect('home')
                except ObjectDoesNotExist:
                    messages.error(request, 'User not found. Please try again.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        # Pre-fill email from session if available
        initial_email = request.session.get('verification_email', '')
        form = EmailVerificationForm(initial={'email': initial_email})
    
    return render(request, 'registration/verify_email.html', {'form': form})


def resend_verification(request):
    """Resend verification OTP"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                if user.is_active:
                    messages.info(request, 'This email is already verified.')
                    return redirect('login')
                
                # Use fixed OTP for development
                otp = "123456"
                
                # Store OTP in cache with 10-minute expiration
                cache.set(f'otp_signup_{email}', otp, 600)
                
                # For development, just notify that OTP is fixed
                print(f"FIXED OTP for {email}: {otp}")
                
                messages.success(request, f'Use OTP {otp} to verify your email.')
                request.session['verification_email'] = email
            except ObjectDoesNotExist:
                messages.error(request, 'No account found with this email.')
        else:
            messages.error(request, 'Please provide an email address.')
    
    return render(request, 'registration/resend_verification.html')


def password_reset_request(request):
    """Request password reset with OTP"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    messages.error(request, 'This account is not verified. Please verify your email first.')
                    return redirect('resend_verification')
                
                # Use fixed OTP for development
                otp = "123456"
                
                # Store OTP in cache with 10-minute expiration
                cache.set(f'otp_reset_{email}', otp, 600)
                
                # For development, just notify that OTP is fixed
                print(f"FIXED OTP for {email}: {otp}")
                
                messages.success(request, f'Use OTP {otp} to reset your password.')
                # Store email in session for verification
                request.session['reset_email'] = email
                return redirect('password_reset_verify')
            except ObjectDoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'registration/password_reset_request.html', {'form': form})


def password_reset_verify(request):
    """Verify OTP and reset password"""
    if request.method == 'POST':
        form = PasswordResetVerifyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            entered_otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password1']
            
            # Get stored OTP
            stored_otp = cache.get(f'otp_reset_{email}')
            
            if stored_otp and entered_otp == stored_otp:
                # OTP verified successfully
                try:
                    user = User.objects.get(email=email)
                    # Set new password
                    user.password = make_password(new_password)
                    user.save()
                    messages.success(request, 'Password reset successfully!')
                    # Clear OTP from cache
                    cache.delete(f'otp_reset_{email}')
                    # Clear session
                    if 'reset_email' in request.session:
                        del request.session['reset_email']
                    return redirect('login')
                except ObjectDoesNotExist:
                    messages.error(request, 'User not found. Please try again.')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        # Pre-fill email from session if available
        initial_email = request.session.get('reset_email', '')
        form = PasswordResetVerifyForm(initial={'email': initial_email})
    
    return render(request, 'registration/password_reset_verify.html', {'form': form})