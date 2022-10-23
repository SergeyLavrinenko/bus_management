from authapp.models import users
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def check_auth(request):
    try:
        resp = None
        code = request.COOKIES["userCode"]
        user = users.objects.filter(code=code)
        if len(user) > 0:
            is_admin = user[0].is_admin
        else:
            resp = redirect('aPage')
    except:
        resp = redirect('aPage')

    return resp, is_admin


def main_admin(request):
    auth, is_admin = check_auth(request)
    if auth != None:
        return auth
    if not is_admin:
        return redirect("main")

    response = render(request, 'html/main.html', {"host": request.get_host()})
    return response