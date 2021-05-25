from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings as s
import json
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'index.html')

@login_required(login_url='/auth/login/')
def expenses(request):
    return render(request,'expenses.html')

@login_required(login_url='/auth/login/')
def settings(request):
    curr=[]
    file=os.path.join(s.BASE_DIR,'data.json')
    with open(file) as f:
        item=json.load(f)
        for i,j in item.items():
            curr.append({'name':i, 'value':i+"-"+j})
    user=request.user
    sett="Choose Currency"
    if request.method=="GET":
        try:
            sett=Userpref.objects.get(username=user)
            print(sett)
            context={
                'prev':sett.currency,
                'curr':curr
        }
        except Userpref.DoesNotExist as e:
            context={
                'prev':sett,
                'curr':curr
        }
        return render(request,'userpref.html',context=context)
    else:
        try:
            sett=Userpref.objects.get(username=user)
        except Userpref.DoesNotExist as e:
            sett=Userpref.objects.create(username=user)

        sett=Userpref.objects.get(username=user)
        val=request.POST['currency']
        sett.currency=val
        sett.save()
        messages.success(request,"Setting saved successfully")
        return render(request,'index.html')


def expensesadd(request):
    if request.method == 'POST':
        user=request.user
        amount=request.POST['amount']
        category=request.POST['category']
        date=request.POST['date']
        description=request.POST['description']
        user=User.objects.get(username=user)
        print(amount, category, date, description)
        ent=Expenses.objects.create(owner=user, amount=amount, category=category, date=date, description=description)
        ent.save()
        messages.success(request,"New record added successfully")
        return render(request,'index.html')
    category=Category.objects.all()
    context={
        'category':category
    }
    return render(request,'expensesadd.html',context)


def expensesedit(request,id):
    pass