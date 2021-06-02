from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings as s
import json
from expenses.models import Userpref
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
import datetime
import csv
# Create your views here.


def dahboard(request):
    return render(request,'dashboard.html')

@login_required(login_url='/auth/login/')
def expenses(request):
    data=Expenses.objects.filter(owner=request.user)
    try:
        pref=Userpref.objects.get(username=request.user)
    except:
        pref=" "

    paginator = Paginator(data, 5)
    page_number = request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    context={'pref':pref,'data':data,'page_obj': page_obj}
    return render(request,'expenses.html',context=context)

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
            # print(sett)
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


@login_required(login_url='/auth/login/')
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
        return redirect('expenses:expenses')
    category=Category.objects.all()
    context={
        'category':category
    }
    
    return render(request,'expensesadd.html',context)

@login_required(login_url='/auth/login/')
def expensesedit(request,id):
    if request.method=='GET':
        ele=Expenses.objects.get(id=id)
        context={
            'edit':True,
            'ele':ele,
            'category':Category.objects.all()
        }
        return render(request,'expensesadd.html',context)

    if request.method=='POST':
        ele=Expenses.objects.get(id=id)
        ele.amount=request.POST['amount']
        ele.category=request.POST['category']
        ele.date=request.POST['date']
        ele.description=request.POST['description']
        ele.save()
        messages.success(request,"Editted successfully")
        return redirect('expenses:expenses')

@login_required(login_url='/auth/login/')
def expensesdelete(request,id):
    ele=Expenses.objects.get(id=id)
    ele.delete()
    messages.success(request,"Deleted Successfull")
    return redirect('expenses:expenses')

def stat(request):
    return render(request,'stats.html')

def getcat(exp):
    return exp.category
    

def stat_api(request):
    now=datetime.datetime.today()
    year=now-datetime.timedelta(days=30*12)
    exp=Expenses.objects.filter(owner=request.user,date__gte=year,date__lte=now)
    final={}
    all_cat=[]
    f=Category.objects.all()
    for i in f:
        all_cat.append(i.name)
        
    def get_amt(cat):
        ans=0
        expd=exp.filter(category=cat)
        for i in expd:
            ans+=int(i.amount)
        return ans

    for y in all_cat:
        final[y]=get_amt(y)

    return JsonResponse({'exp_result':final},safe=False)

@login_required(login_url='/auth/login/')
def exportdata(request):
    data=Expenses.objects.filter(owner=request.user)
    res=HttpResponse(content_type='text/csv')
    res['Content-Disposition']='attachment; filename=Expense_Data'+str(datetime.datetime.now())+'.csv'
    writer=csv.writer(res)
    writer.writerow(['Amount','Category','Date','Description'])

    for i in data:
        writer.writerow([i.amount,i.category,i.date,i.description])
    return res