from django.contrib import admin
from .models import Profile, TelegramOTP


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "info"]


@admin.register(TelegramOTP)
class TelegramOtpAdmin(admin.ModelAdmin):
    list_display = ['id' ,'telegram_user_id', 'otp']