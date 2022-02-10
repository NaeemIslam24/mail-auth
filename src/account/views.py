from ast import Not
from email import message
import imp
from logging import exception
import profile
from re import template
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
#sent mail
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import uuid
from account.models import Profile
# Create your views here.

def login_auth(request):

    template = 'login.html'
    if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = User.objects.filter(username = username).first()

      if user is None:
          messages.error(request, 'User not found')
          return redirect('login')
      profile = Profile.objects.filter(user = user).first()

      if not profile.is_verified:
          messages.error(request, 'Not verified check your Email')
          return redirect('login')
          
      user_obj = authenticate(request, username=username, password=password)

      if user_obj is not None:

            login(request, user)
            return redirect('home')

      else:

          messages.success(request, 'Login not successful')
          
          return redirect('login')

    return render(request, template_name=template)




def register(request):

    template = 'register.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_pass')
        try:
            if password == confirm_password:
                if User.objects.filter(username = username).exists():
                    messages.error(request, 'Username taken already')
                    return redirect('register')
                if User.objects.filter(email = email).exists():
                    messages.error(request, 'Email taken already')
                    return redirect('register')
                user_obj = User.objects.create(username = username, email = email)
                user_obj.set_password(password)
                user_obj.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)          
                profile_obj.save()
                sent_registation_mail(email, auth_token, username)
                return redirect('token')
            else:
                messages.error(request, 'Password and confirm password not matched')
                return redirect('register')
        except Exception as e:
            print(e)

    return render(request, template_name=template)


def success(request):

    template = 'success.html'

    return render(request, template_name=template)

def verify(request, auth_token):
    try:
        prof = Profile.objects.filter(auth_token = auth_token).first()

        if prof:
            if prof.is_verified:

                messages.success(request, 'Your account is already verified')
                return redirect('login')

            prof.is_verified = True
            prof.save()
            messages.success(request, 'Your account has been verified')
            return redirect('login')
        else:
            return redirect('/error')
        
    except Exception as e:
        print(e)
        
    return redirect('/')


def token(request):

    template = 'token.html'
    if request.method == 'POST':
      code = request.POST.get('code')
      profile_code = Profile.objects.filter(auth_token = code).first()

      if profile_code:
          if profile_code.is_verified:
              messages.success(request, 'Your account alredy has been verified')
              return redirect('login')
     
          profile_code.is_verified = True
          profile_code.save()
          messages.success(request, 'Your account has been verified')
          return redirect('login')
      else:
          return redirect('error')



    return render(request, template_name=template)



def error(request):

    template = 'token.html'

    return render(request, template_name=template)


def sent_registation_mail(email, token, username):
    subject = 'Your accounts need to be verified'
    message = f'Hi {username}! Here is the CODE  "{token}"  please click the link to verify your account http://127.0.0.1:8000/verify/{token}'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

@login_required
def home(request):
    template = 'home.html'
    
    return render(request, template_name=template)

