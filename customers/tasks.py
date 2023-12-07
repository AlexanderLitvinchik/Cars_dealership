from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from .models import Customer


@shared_task
def send_confirmation_email_task(user_id):
    # breakpoint()
    user = Customer.objects.get(user_id=user_id)
    expiration_time = datetime.utcnow() + timedelta(hours=24)
    access_token = AccessToken.for_user(user.user)
    access_token.set_exp(int(expiration_time.timestamp()))

    token = str(access_token)
    # confirmation_url = f'http://127.0.0.1:8000/confirm-registration/?token={token}'

    subject = 'Confirm Registration'
    message = f'Your token to confirm registration: {token}'

    from_email = None
    to_email = user.user.email

    send_mail(subject, message, from_email, [to_email])
