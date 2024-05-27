
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .forms import RegisterForm


# def register(request):
#     """
#     View for user registration.
#     """
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'VibeMeet_app/login.html', {'success': "Registration successful. Please login."})
#         else:
#             error_message = form.errors.as_text()
#             return render(request, 'VibeMeet_app/register.html', {'error': error_message})
#     else:
#         form = RegisterForm()
#     return render(request, 'VibeMeet_app/register.html', {'form': form})

# def login_view(request):
#     """
#     View for user login.
#     """
#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("/dashboard")
#         else:
#             return render(request, 'VibeMeet_app/login.html', {'error': "Invalid credentials. Please try again."})
#     return render(request, 'VibeMeet_app/login.html')

# @login_required
# def dashboard(request):
#     """
#     Dashboard view after user login.
#     """
#     return render(request, 'VibeMeet_app/dashboard.html', {'name': request.user.first_name})

# @login_required
# def videocall(request):
#     return render(request, 'VibeMeet_app/videocall.html', {'name':request.user.first_name + " " + request.user.last_name})

# @login_required
# def logout_view(request):
#     """
#     View for user logout.
#     """
#     logout(request)
#     return redirect("/login")

# @login_required
# def join_room(request):
#     if request.method == 'POST':
#         roomID = request.POST['roomID']
#         return redirect("/meeting?roomID=" + roomID)
#     return render(request, 'VibeMeet_app/joinroom.html')



from VibeMeet_app.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dash_board(request):
    """
    Dashboard view after user login.
    """
    return render(request, 'dashboard.html', {'name': request.user.username})



def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        
        login(request , user)
        return redirect('/dashboard')

    return render(request , 'login.html')




def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'register.html')

def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')








def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )




def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            token = str(uuid.uuid4())
            profile = Profile.objects.get(user=user)
            profile.auth_token = token
            profile.save()
            send_password_reset_email(email, token)
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('/accounts/login')
        else:
            messages.error(request, 'User with this email does not exist.')
    return render(request, 'password_reset_request.html')
    

def reset_password(request, token):
    try:
        profile = Profile.objects.get(auth_token=token)
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user = profile.user
                user.set_password(new_password)
                user.save()
                profile.password_reset_token = ''
                profile.save()
                messages.success(request, 'Password has been reset successfully.')
                return redirect('/accounts/login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'reset_password.html', {'token': token})
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid link')
        return redirect('/error')
    


def send_password_reset_email(email, token):
    subject = 'Reset Your Password'
    message = f'Hi, click the link to reset your password: http://127.0.0.1:8000/reset_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)



@login_required
def videocall(request):
    return render(request, 'videocall.html', {'name':request.user.username})


@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')
 


@login_required
def logout_view(request):
    """
    View for user logout.
    """
    logout(request)
    return redirect('/accounts/login')

