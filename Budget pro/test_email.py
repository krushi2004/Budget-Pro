import os
import django
from django.conf import settings
from django.core.mail import EmailMessage

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budgetpro.settings')
django.setup()

def test_email_sending():
    """Test email sending functionality"""
    try:
        # Check if email settings are configured
        if not settings.EMAIL_HOST_USER:
            print("Email settings not configured. Printing to console instead:")
            print("=== EMAIL OTP ===")
            print("To: test@example.com")
            print("Subject: Budget Pro Verification Code")
            print("Message: Your verification code is: 123456")
            print("==============")
            return True
            
        # Send actual email
        email_message = EmailMessage(
            subject='Budget Pro Test Email',
            body='This is a test email from Budget Pro.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=['test@example.com']
        )
        email_message.send()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == "__main__":
    test_email_sending()