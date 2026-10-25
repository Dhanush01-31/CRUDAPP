import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

logger = logging.getLogger(__name__)

def send_welcome_email(request=None, username='', password='', Name='', usermail=''):
    """
    Sends a welcome email to the newly registered user.
    Catches and logs any SMTP / connection exceptions to prevent registration failure.
    """
    try:
        html_content = render_to_string(
            "email/welcome_email.html",
            {
                'username': username,
                'password': password,
                'Name': Name
            }
        )

        email = EmailMultiAlternatives(
            subject="Welcome to our CRUD App Platform",
            body=f"Hello {username}, your account has been created successfully.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[usermail]
        )
        email.attach_alternative(html_content, 'text/html')
        email.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email to {usermail}: {e}")
        return False
