from core.celery import app
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import get_user_model
from django.http import Http404
from allauth.account.models import EmailAddress


@app.task()
def send_confirmation_email(user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404("User not found.")

    email_address = EmailAddress.objects.get(user=user, primary=True)
    email_address.send_confirmation()
