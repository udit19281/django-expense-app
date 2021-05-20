from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='auth'

urlpatterns = [
    path('login/',views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('reset/',views.reset, name='reset'),
    path('valid-email/',csrf_exempt(views.ValidateEmail.as_view())),
]