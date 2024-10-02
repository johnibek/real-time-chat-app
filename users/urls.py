from django.urls import path
from . import views


urlpatterns = [
    path("", views.profile_view, name='profile'),
    path("edit/", views.profile_edit_view, name='profile_edit'),
    path("onboarding/", views.profile_edit_view, name='profile-onboarding'),
    path("settings/", views.profile_settings_view, name='profile_settings'),
    path("emailchange/", views.profile_email_change, name='profile_emailchange'),
    path("emailverify/", views.profile_email_verify, name='profile_emailverify'),
    path("delete/", views.profile_delete_view, name='profile_delete'),
]
