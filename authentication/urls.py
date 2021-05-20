from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
app_name='auth'

urlpatterns = [
    path('login/',views.Login.as_view(), name='login'),
    path('logout/',views.Logout.as_view(), name='logout'),
    path('signup/',views.signup, name='signup'),
    path('reset/',views.reset, name='reset'),
    path('valid-email/',csrf_exempt(views.ValidateEmail.as_view())),
    path('valid-username/',csrf_exempt(views.ValidateUsername.as_view())),
    path('activate/<uid>/<token>',views.activate.as_view(),name="activate")
]