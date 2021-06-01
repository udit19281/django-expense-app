from django.shortcuts import redirect, render
from .models import *
from expenses.models import Userpref
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings as s
import json
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.

@login_required(login_url='/auth/login/')
def income(request):
    data=Income.objects.filter(owner=request.user)
    try:
        pref=Userpref.objects.get(username=request.user)
    except:
        pref=" "

    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={'pref':pref,'data':data,'page_obj': page_obj}
    return render(request,'income/income.html',context=context)

@login_required(login_url='/auth/login/')
def incomeadd(request):
    if request.method == 'POST':
        user=request.user
        amount=request.POST['amount']
        source=request.POST['source']
        date=request.POST['date']
        description=request.POST['description']
        user=User.objects.get(username=user)
        print(amount, source, date, description)
        ent=Income.objects.create(owner=user, amount=amount, source=source, date=date, description=description)
        ent.save()
        messages.success(request,"New record added successfully")
        return redirect('income:income')
    source=Source.objects.all()
    context={
        'source':source
    }
    
    return render(request,'income/incomeadd.html',context)

@login_required(login_url='/auth/login/')
def incomeedit(request,id):
    if request.method=='GET':
        ele=Income.objects.get(id=id)
        context={
            'edit':True,
            'ele':ele,
            'source':Source.objects.all()
        }
        return render(request,'income/incomeadd.html',context)

    if request.method=='POST':
        ele=Income.objects.get(id=id)
        ele.amount=request.POST['amount']
        ele.source=request.POST['source']
        ele.date=request.POST['date']
        ele.description=request.POST['description']
        ele.save()
        messages.success(request,"Editted successfully")
        return redirect('income:income')

@login_required(login_url='/auth/login/')
def incomedelete(request,id):
    ele=Income.objects.get(id=id)
    ele.delete()
    messages.success(request,"Deleted Successfull")
    return redirect('income:income')

def stat(request):
    return render(request,'income/stats.html')

def getcat(exp):
    return exp.source
    

def stat_api(request):
    now=datetime.datetime.today()
    year=now-datetime.timedelta(days=30*12)
    exp=Income.objects.filter(owner=request.user,date__gte=year,date__lte=now)
    final={}
    # print(exp)
    # print(Income.objects.all())
    all_cat=[]
    f=Source.objects.all()
    for i in f:
        all_cat.append(i.name)
        
    def get_amt(cat):
        ans=0
        expd=exp.filter(source=cat)
        for i in expd:
            ans+=int(i.amount)
            # print(i.amount)
        return ans

    for y in all_cat:
        final[y]=get_amt(y)

    return JsonResponse({'inc_result':final},safe=False)

