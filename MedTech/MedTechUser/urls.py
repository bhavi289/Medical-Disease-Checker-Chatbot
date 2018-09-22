from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'MedTechUser'

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'send-message/$', views.sendMessage, name="send-message"),
    url(r'home2/$', views.home2, name="home2"),
    url(r'insert_data/$', views.insertData, name="insert_data" ),
    url(r'query_feeling', views.query_feeling, name="query_feeling")
]