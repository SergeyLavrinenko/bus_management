from authapp.models import users
from django.shortcuts import render, redirect
from hashlib import sha1

# Create your views here.
def authPage(request, mess = ""):
    response = render(request, 'html/template/auth.html', {'mess': mess})
    return response

def authPageLog(request):
    print("a")
    return authPage(request, "Такого логина не существует")

def authPagePas(request):
    return authPage(request, "Неверный пароль")

def auther(request):
    password = ""
    login = ""
    if request.method == "POST":
        login = request.POST.get('login')
        password = request.POST.get('pass')

    usersObj = users.objects.filter(login = login)

    password_b = str.encode(password)
    print(password)
    print(sha1(password_b).hexdigest())
    if len(usersObj) > 0:
        if usersObj[0].password == sha1(password_b).hexdigest():
            response = render(request, 'html/authRedirect.html', {})
            response.set_cookie("userCode", usersObj[0].code)
            return response
        else:
            return redirect("aPagePas")
    else:
        return redirect("aPageLog")

def authRedirect(request):
    return render(request, 'html/authRedirect.html', {})