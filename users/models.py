from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static  # It is needed to display profile avatar images


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.user.username


    @property
    def name(self):
        if self.displayname:
            name = self.displayname
        else:
            name = self.user.username
        return name


    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar.svg")
        return avatar
    

class TelegramOTP(models.Model):
    telegram_user_id = models.CharField(max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


