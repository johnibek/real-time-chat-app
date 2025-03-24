from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

from .models import Profile
from .tasks import send_confirmation_email


@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    # Add profile if user is created
    if created:
        Profile.objects.create(user=instance)
    else:
        # Update allauth email address if exists
        try:
            email_address = EmailAddress.objects.get_primary(instance)
            if email_address.email != instance.email:
                email_address.email = instance.email
                email_address.verified = False
                email_address.save()
        except:
            # If allauth email address does not exist, create one
            EmailAddress.objects.create(
                user=instance,
                email=instance.email,
                primary=True,
                verified=False
            )


@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()


@receiver(user_signed_up)  # Send verification code after user has been signed up. Email sending is overtaken by celery.
def send_verification_email(request, user, **kwargs):
    send_confirmation_email.delay(user.id)
