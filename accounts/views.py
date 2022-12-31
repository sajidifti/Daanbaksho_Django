from django.shortcuts import render, redirect
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from daanbaksho import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str as force_text
from django.contrib.auth import login
from . tokens import generate_token
from . decorators import *

# Create your views here.

# Volunteer Signup
# @unauthenticated_user


def volunteerSignUp(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='volunteer')
            user.groups.add(group)

            messages.success(
                request, f'Acoount was successfully created for {username}. Please check your email to activate your account')

            # Welcome Email
            subject = "Welcome to Daanbaksho!!"
            message = "Hello " + user.first_name + "!! \n" + \
                "Welcome to Daanbaksho!! \nThank you for signing up.\nYou are signed up for a great cause. Your labour contributions will make a difference.\n\n We have received your request to sign up as a volunteer. We will verify your request and get back to you as soon as possible. Keep an eye on your email inbox. We will send you confirmation email after verifying. \n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            return redirect('home')

    else:
        form = SignUpForm()

    context = {'form': form,
               'type': 'Volunteer'}

    return render(request, 'userSignUp.html', context)


# Donor Signup
# @unauthenticated_user
def donorSignUp(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='donor')
            user.groups.add(group)

            messages.success(
                request, f'Acoount was successfully created for {username}. Please check your email to activate your account')

            # Welcome Email
            subject = "Welcome to Daanbaksho!!"
            message = "Hello " + user.first_name + "!! \n" + \
                "Welcome to Daanbaksho!!\nThank you for signing up.\nYou are signed up for a great cause.Your donations will make a difference.\n\n We have also sent you a confirmation email, please confirm your email address.\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email - Daanbaksho"
            message2 = render_to_string('email_confirmation.html',
                                        {
                                            'name': user.first_name,
                                            'domain': current_site.domain,
                                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token': generate_token.make_token(user)
                                        })
            email = EmailMessage(email_subject, message2,
                                 settings.EMAIL_HOST_USER, [user.email])
            email.fail_silently = True
            email.send()

            return redirect('login')

    else:
        form = SignUpForm()

    context = {'form': form,
               'type': 'Donor'}

    return render(request, 'userSignUp.html', context)

# Activation


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')


# Home
# @login_required
# @admin_only
def home(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(
                request, f'Your Acoount was successfully Updated')

            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)


# Volunteer Confirmation View
@login_required
@volunteer_coordinator_only
def volunteerConfirmation(request):
    userList = User.objects.all()

    if request.method == 'POST':

        myuser = User.objects.get(id=request.POST.get("user_id"))

        if request.POST.get("status") == 'Accept':
            current_site = get_current_site(request)
            email_subject = "Confirm your Email - Daanbaksho"
            message2 = render_to_string('email_confirmation.html',
                                        {
                                            'name': myuser.first_name,
                                            'domain': current_site.domain,
                                            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                                            'token': generate_token.make_token(myuser)
                                        })
            email = EmailMessage(email_subject, message2,
                                 settings.EMAIL_HOST_USER, [myuser.email])
            email.fail_silently = True
            email.send()

            messages.success(
                request, "Confirmation Email Sent to {myuser.email}")

        elif request.POST.get("status") == 'Decline':
            myuser.delete()

            subject = "Request Denied - Daanbaksho"
            message = "Hello " + myuser.first_name + "!! \n" + \
                "We are extremely sorry to inform you that your request to sign up as a volunteer was denied. Please try again later.\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.danger(
                request, "Request to Sign Up as Volunteer of {myuser.username}Denied. Denial Email Sent to {myuser.email}.")

    return render(request, 'volunteer_confirmation.html', {'users': userList})


# Volunteer List

def volunteerList(request):
    userList = User.objects.all()

    if request.method == 'POST':

        myuser = User.objects.get(id=request.POST.get("user_id"))

        if request.POST.get("status") == 'Terminate':
            myuser.delete()

            subject = "You have been terminated - Daanbaksho"
            message = "Hello " + myuser.first_name + "!! \n" + \
                "We are extremely sorry to inform you that you have been terminated.\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(
                request, "termination Email Sent to " + myuser.email)

            return redirect('volunteer_list')

        elif request.POST.get("status") == 'Ban':
            myuser.is_active = False

            subject = "You have been banned - Daanbaksho"
            message = "Hello " + myuser.first_name + "!! \n" + \
                "We are extremely sorry to inform you that you have been banned.\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.danger(
                request, "Volunteer Banned")

            return redirect('volunteer_list')

    return render(request, 'volunteer_list.html', {'users': userList})


# SignUp
@unauthenticated_user
def signup(request):
    return render(request, 'signup.html')


def dashboard(request):
    return render(request, 'dashboard.html')