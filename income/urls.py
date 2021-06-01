
from django.contrib import admin
from django.urls import path,include
from . import views
app_name="income"

urlpatterns = [
    path('',views.income, name='income'),
    path('add/',views.incomeadd, name='add'),
    path('edit/<int:id>',views.incomeedit, name='edit'),
    path('delete/<int:id>',views.incomedelete, name='delete'),
    path('stat/',views.stat, name='stat'),
    path('statapi/',views.stat_api, name='statapi'),
    path('data/',views.exportdata, name='export'),
]
