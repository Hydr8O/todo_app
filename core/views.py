from django.shortcuts import render, redirect

def redirect_signup(request):
    return redirect('auth_app:signup')