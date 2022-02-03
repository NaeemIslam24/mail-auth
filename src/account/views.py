from re import template
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

import uuid

from account.models import Profile
# Create your views here.

def login(request):

    template = 'login.html'

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
                profile_obj = Profile.objects.create(user = user_obj, auth_token = str(uuid.uuid4))          
                profile_obj.save()
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


def token(request):

    template = 'token.html'

    return render(request, template_name=template)