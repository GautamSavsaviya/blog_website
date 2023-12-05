from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .tokens import generattoken
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required

# Create your views here.


def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user.is_active = False
            user.save()
            messages.success(
                request, f"You are successfully regiserted..!, We will send you a confirmation mail to validate your email id")

            # Send welcome mail
            subject = 'Welcome to our platform'
            message = f"Welcome {user.first_name} {user.last_name} to our website\n We will send you confirmation mail for your email authentication. Please confirm your email in order to active your account.\n\nThak you\nAdmin"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=True)

            # Send confirmation mail for validate email id
            current_site = get_current_site(request)
            subject = "Confirmation mail"
            message = render_to_string('users/email-confirmation.html', {
                'name': f"{user.first_name} {user.last_name}",
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generattoken.make_token(user),
            })
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(
                subject, message, from_email, recipient_list, fail_silently=True
            )

            return redirect('users:login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'users/signup.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if not User.objects.get(username=username).is_active:
            messages.error(
                request, 'Your account is deactivate. please, first activate by clicking link that send you via mail...!')
            return redirect('users:login')

        if user is not None:
            login(request, user)
            return redirect('blogs:index')
        else:
            messages.error(request, 'Username and password does not exist...!')
            return redirect('users:login')

    return render(request, 'users/login.html')


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        return redirect('users:login')
    else:
        return render(request, 'users/authentication-failed.html')


@login_required(login_url='users:login')
def profile(request):
    if request.method == "POST":
        mobile = request.POST["mobile"]
        location = request.POST["location"]
        image = request.FILES['image']

        profile = Profile.objects.get(user=request.user)
        profile.mobile = mobile
        profile.location = location
        profile.image = image
        profile.save()

        return redirect('blogs:index')
    return render(request, 'users/profile.html')
