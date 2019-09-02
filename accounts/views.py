# from django.shortcuts import render, redirect

# from django.contrib.auth import (
#     authenticate, 
#     get_user_model,
#     login,
#     logout
# )

# from .forms import UserLoginForm, UserRegisterForm

# def login_view(request):
#     next = request.GET.get('next')
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect('/')

#     context = {
#         'form': form,
#     }
#     return render(request, "login.html", context)

# def register_view(request):
#     next = request.GET.get('next')
#     form = UserRegisterForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         password = form.cleaned_data.get('password')
#         user.set_password(password)
#         user.save()
#         user = authenticate(username=user.username, password=password)
#         login(request, user)
#         if next:
#             return redirect(next)
#         return redirect('/')

#     context = {
#         'form': form,
#     }
#     return render(request, "signup.html", context)

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
import re
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import JsonResponse
import datetime
from django.http import QueryDict


class RegisterView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if request.user.is_authenticated:  #logout first
            return JsonResponse({'error': {'message': 'Please Logout first', 'statusCode': '400'}}, status=400)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if not len(username):
            return JsonResponse({'error': {'message': 'Provide a username', 'statusCode': '400'}}, status=400) 
        if User.objects.filter(username = username):  #username exists
            return JsonResponse({'error': {'message': 'Username already exists', 'statusCode': '400'}}, status=400)
        if User.objects.filter(email = email):  #email exists
            return JsonResponse({'error': {'message': 'Email already exists', 'statusCode': '400'}}, status=400)
        msg = passValidator(password)  #pass check
        if msg:
            return JsonResponse({'error': {'message': msg, 'statusCode': '400'}}, status=400)
        if not re.fullmatch(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return JsonResponse({'error': {'message': 'Not a valid email', 'statusCode': '400'}}, status=400) #email check
        user = User.objects.create_user(username, email, password)
        user.save()
        return JsonResponse({'data': {'message': 'Successfully registered id:'+ str(user.id)}})

class LoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'data': {'message': 'Successfully logged in'}})
        elif User.objects.filter(username = username):
            return JsonResponse({'error': {'message': 'Incorrect password', 'statusCode': '400'}}, status=400)
        else:
            return JsonResponse({'error': {'message': 'User does not exist', 'statusCode': '400'}}, status=400)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return JsonResponse({'data': {'message': 'Sucessfully logged out'}})

class CheckAuthView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({'data': {'message': 'You are authenticated id: '+str(request.user.id)}})
        else:
            return JsonResponse({'data': {'message': 'Please authenticate first'}})

class ChangePasswordView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ChangePasswordView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': {'message': 'You are not authenticated', 'statusCode': '400'}}, status=400)
        logout(request)
        username = request.POST['username']
        password = request.POST['password']
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        return JsonResponse({'data': {'message': 'Password changed successfully'}})

def passValidator(password):
    msg = "Password should contain minimum 8 characters, a lowercase character, an uppercase character, a numeric character and a special character"
    if (len(password)<8): 
        return msg
    elif not re.search("[a-z]", password): 
        return msg
    elif not re.search("[A-Z]", password): 
        return msg
    elif not re.search("[0-9]", password): 
        return msg
    elif not re.search("[_@$]", password): 
        return msg
    elif re.search("\s", password): 
        return msg
    return 0
