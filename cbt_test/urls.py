from django.contrib import admin
from django.urls import path,include
from cbt import settings
from cbt_test import views
from django.conf.urls.static import static


urlpatterns = [
    path("",views.login_user),
    path("login",views.login_user),
    path("add_user",views.add_user),
    path('index',views.index),
    path('questions',views.question),
    path('set_question',views.set_question),
    path('score',views.score),
    path('dashboard',views.dashboard),
    path('set_test',views.set_test),
    path('signout',views.signout),
    path('blank',views.blank),
    path('result_analysis',views.result)
    
    
]