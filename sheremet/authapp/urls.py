from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'auth', views.auther, name='auther'),
    re_path(r'authRe', views.authRedirect, name='authRedirect'),

    re_path(r'-', views.authPageLog, name = 'aPageLog'),
    re_path(r'=', views.authPagePas, name = 'aPagePas'),
    re_path(r'', views.authPage, name = 'aPage'),

]