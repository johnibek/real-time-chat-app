from allauth.account.models import EmailAddress
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from .models import Profile


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

