from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'MedTechUser'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'send-message/$', views.sendMessage, name="send-message")
]