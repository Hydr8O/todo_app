from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from auth_app.exceptions import PasswordMismatchException, UserAlreadyExistsException, WrongCredentialsException, UserActivationException
from auth_app.tokens import generate_activation_token, check_activation_token


def signup_user(request):
    '''Takes credentials from post request and adds new user to the database'''
    user_credentials = __get_user_credentials(request)
    try:
        created_user = __create_new_user(user_credentials)
        _send_activation_email(created_user, request)
        return redirect('auth_app:login')
    except PasswordMismatchException as error:
        messages.error(request, error.message)
        return redirect('auth_app:signup')
    except UserAlreadyExistsException as error:
        messages.error(request, error.message)
        return redirect('auth_app:signup')

def __create_new_user(user_credentials):
    username = user_credentials.get('username')
    password = user_credentials.get('password')
    email = user_credentials.get('email')
    confirm = user_credentials.get('confirm')

    if password == confirm:
        try:
            return User.objects.create_user(
                username=username, 
                password=password,
                email=email,
                is_active=False
            )
        except IntegrityError:
            raise UserAlreadyExistsException
    else:
        raise PasswordMismatchException 

def _send_activation_email(user, request):
    email = _construct_activation_email(user, request)
    user.email_user(email.get('mail_subject'), email.get('message'))


def _construct_activation_email(user, request):
    activation_token = generate_activation_token(user)
    mail_subject = 'Account activation'
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    message = render_to_string('auth_app/activation_email.html', {
        'domain': domain,
        'uid': uid,
        'token': activation_token
    })
    return {
        'mail_subject': mail_subject,
        'message': message
    }

def activate_user(request, token, uid):
    user_id = force_text(urlsafe_base64_decode(uid))
    user = User.objects.get(pk=user_id)
    if check_activation_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Account {user.username} has been activated succesfully')
        return redirect('auth_app:login')
    else:
        messages.error(request, 'Activation error. Perhaps you have used the same link more then once')
        return redirect('auth_app:login')
    

def login_user(request):
    user_credentials = __get_user_credentials(request)
    username = user_credentials.get('username')
    password = user_credentials.get('password')
    try:
        authenticated_user = __authenticate_user(request, username, password)
        login(request, authenticated_user)
        return redirect('todo_app:current_todos')
    except WrongCredentialsException as error:
        messages.error(request, error.message)
        return redirect('auth_app:login')
    
def __authenticate_user(request, username, password):
    user = authenticate(
        request, 
        username=username, 
        password=password
    )

    if user is None:
        raise WrongCredentialsException
    else:
        return user

def __get_user_credentials(request):
    post = request.POST
    user_credentials = {
        'username': post.get('username'),
        'password': post.get('password'),
        'confirm': post.get('confirm'),
        'email': post.get('email')
    } 
    return user_credentials 


def logout_user(request):
    logout(request)
    return redirect('auth_app:login')