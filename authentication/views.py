from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from authentication.forms import SignUpForm, LoginForm
from subscription.models import SubscribedUser


def signup(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            return render(request, 'signup.html',
                          {'form': form})

        else:
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password,
                                     email=email)
            user = authenticate(username=username, password=password)
            login(request, user)
            SubscribedUser.subscribe(email=email)
            return redirect('/')

    else:
        return render(request, 'signup.html',
                      {'form': SignUpForm()})


def log_in(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if not form.is_valid():
                return render(request, 'login.html',
                          {'form': form})
            else:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'login.html',
                          {'form': LoginForm()})