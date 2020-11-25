from django.shortcuts import render, redirect
from auth_app.auth_service import signup_user, login_user, logout_user, activate_user

def signup(request):
    if request.method == "POST":
       return signup_user(request)
    else:
        return render(
            request,
            'auth_app/signup.html'
        )

def login(request):
    if request.method == "POST":
        return login_user(request)
    else:
        return render(
            request,
            'auth_app/login.html'
        )

def logout(request):
    return logout_user(request)

def activate(request, token, uid):
    return activate_user(request, token, uid)
