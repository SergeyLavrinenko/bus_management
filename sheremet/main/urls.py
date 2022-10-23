from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'setting', views.Setting, name = "setting"),
    re_path(r'ajax/getTime', views.getTime, name="getTime"),
    re_path(r'logout', views.logout, name="logout"),
    re_path(r'', views.main, name = "main"),


]