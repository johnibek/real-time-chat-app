from allauth.account.utils import send_email_confirmation
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from .forms import ProfileForm, EmailForm


def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('account_login')
    return render(request, "users/profile.html", {'profile': profile})


@login_required
def profile_edit_view(request):
    # print(request.META["HTTP_REFERER"])  # http://127.0.0.1:8000/profile/
    form = ProfileForm(instance=request.user.profile)

    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False

    return render(request, 'users/profile_edit.html', {'form': form, 'onboarding': onboarding})


@login_required
def profile_settings_view(request):
    return render(request, 'users/profile_settings.html', {})


@login_required
def profile_email_change(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form': form})

    if request.method == 'POST':
        form = EmailForm(instance=request.user, data=request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect('profile_settings')
            form.save()

            # The signal updates emailaddress and set verified to False

            # Then send confirmation email
            send_email_confirmation(request, request.user)
            return redirect('profile_settings')
        else:
            messages.warning(request, "Form Not Valid")
            return redirect('profile_settings')

    return redirect('home')


@login_required
def profile_email_verify(request):
    send_email_confirmation(request, request.user)
    messages.success(request, f"Confirmation Email Sent To {request.user.email}")
    return redirect('profile_settings')


@login_required
def profile_delete_view(request):
    if request.method == 'GET':
        return render(request, 'users/profile_delete.html', {})

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Account Deleted")
        return redirect("home")

