import datetime
import math

from authapp.models import users
from main.models import flights, points, roads, bus_drivers, buses, task, working_period
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def check_auth(request):
    try:
        resp = None
        user = [0]
        code = request.COOKIES["userCode"]
        user = users.objects.filter(code=code)
        role = user[0].role
        if len(user) > 0:
            is_admin = user[0].is_admin
        else:
            resp = redirect('aPage')
    except:

        role = 4
        resp = redirect('aPage')

    return resp, role, user[0]

def mainDriver(request):
    auth, role, user = check_auth(request)
    if auth != None:
        return auth

    cur_date = datetime.datetime.now()
    driver_id = bus_drivers.objects.filter(user_id = user.id)[0].id
    work_per = (working_period.objects.filter(bus_driver_id = driver_id) & working_period.objects.filter(to_period__gte = cur_date)).order_by("from_period")
    print(len(work_per))
    tasks = []
    for w_per in work_per:
        bus_id = w_per.bus_id
        print(bus_id)
        buf_tasks = (task.objects.filter(bus_id = bus_id) & task.objects.filter(time_to__gte = cur_date) & task.objects.filter(time_to__lte = w_per.to_period)).order_by("time_from")
        for e in buf_tasks:
            tasks.append(e)

    cur_task = []
    count = 0
    for e in tasks:
        flight_obj = flights.objects.filter(id = e.flight_id)[0]
        cur_task.append({})
        if (flight_obj.arr_dep == "A"):
            cur_task[count]["point_from"] = flight_obj.gate_number
            cur_task[count]["point_to"] = flight_obj.parking_place_number
        else:
            cur_task[count]["point_from"] = flight_obj.parking_place_number
            cur_task[count]["point_to"] = flight_obj.gate_number
        cur_task[count]["time_from"] = e.time_from.strftime("%H:%M")
        cur_task[count]["time_to"] = e.time_to.strftime("%H:%M")
        count += 1


    response = render(request, 'html/driver.html', {"host": request.get_host(), "tasks": cur_task},
                   content_type="text/html")
    return response