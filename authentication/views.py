from django.shortcuts import render
import json
from django.views.generic import View
from expenses.models import User
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import send_mail
import os
from decouple import config
# Create your views here.

def login(request):
    if request.method == 'POST':


        return render(request,'auth/login.html')
    return render(request,'auth/login.html')

def signup(request):
    if request.method == 'POST':
        
        email=request.POST['email']
        password=request.POST['password']
        username=request.POST['username']
        context={
            "fieldvalue":request.POST
        }
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                user=User.objects.create_user(username=username,email=email, password=password)
                user.is_active=False
                user.save()
                #send verification mail
                print(config('EMAIL_HOST'))
                subject="Email Verification"
                body="Test my body"
                send_mail(
                     subject,
                        body,
                        'noreply@uditorg.com',
                    [email],
                    fail_silently=False,
                )
                user.save()
                messages.success(request,"Account Created Successfully!!!")
                return render(request,'auth/signup.html')
            messages.error(request,"User Account Already exists!!!")
            return render(request,'auth/signup.html',context)
        messages.error(request,"Username Already Exists!!!")
        return render(request,'auth/signup.html',context)
        # messages.info(request,"imfo!")
       
        # messages.warning(request,"warming hui hui")

        # return render(request,'auth/login.html')
    return render(request,'auth/signup.html')

def reset(request):
    if request.method == 'POST':

        
        return render(request,'auth/login.html')
    return render(request,'auth/reset.html')


class ValidateEmail(View):
    def post(self, request):
        data=json.loads(request.body)
        email=data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'},status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'email_already exists!'},status=400)
        return JsonResponse({'email_valid':True})