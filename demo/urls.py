from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^demo/welcome$', views.welcome),
    url(r'^demo/index/(?P<id>[0-9]+$)', views.index),
    url(r'^demo/getdata$', views.getdata),
]
