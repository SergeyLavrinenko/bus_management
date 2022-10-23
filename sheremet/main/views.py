import datetime
import math

from authapp.models import users
from main.models import flights, points, roads, bus_drivers, buses, task, working_period
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .functions import *
from math import *
import json
import time
# Create your views here.

def get_time_trip(point_from_id, point_to_id):
    speed_bus = 500 # метров в минуту

    routeA = roads.objects.filter(source_point_id=point_from_id) & roads.objects.filter(target_point_id=point_to_id)
    routeB = roads.objects.filter(source_point_id=point_to_id) & roads.objects.filter(target_point_id=point_from_id)
    min_dist = 20000

    for r in routeA:
        if (r.distance < min_dist):
            min_dist = r.distance
    for r in routeB:
        if (r.distance < min_dist):
            min_dist = r.distance
    if (min_dist == 20000):
        time_trip = 3
    else:
        time_trip = math.ceil(min_dist / speed_bus)

    return time_trip


def update():
    time_plus = 15
    flight = flights.objects.all()
    point_from_id = 0
    point_to_id = 0
    for e in flight:
        if(len(task.objects.filter(flight_id = e.id)) == 0):
            date_cur_flight = datetime.combine(e.date, e.planned_time)
            if(e.arr_dep == "A"):
                point_from = points.objects.filter(location_id = e.gate_number)
                point_to = points.objects.filter(location_id = e.parking_place_number)
            else:
                date_cur_flight -= timedelta(minutes = 30)
                point_to = points.objects.filter(location_id=e.gate_number)
                point_from = points.objects.filter(location_id=e.parking_place_number)

            if (len(point_from) >= 1 and len(point_to) >= 1):
                point_from_id = point_from[0].point_id
                point_to_id = point_to[0].point_id
                time_trip = get_time_trip(point_from_id, point_to_id)
            else:
                time_trip = 3

            work_per = working_period.objects.filter(from_period__lte=date_cur_flight) & working_period.objects.filter(to_period__gte=date_cur_flight)
            best_bus = {}
            heights_bus = []
            for per in work_per:
                cur_bus_id = per.bus_id
                task_bus = (task.objects.filter(time_from__gte = date_cur_flight) & task.objects.filter(time_to__lte = date_cur_flight)) \
                           | (task.objects.filter(time_from__gte = date_cur_flight + timedelta(minutes=time_trip)) & task.objects.filter(time_to__lte = date_cur_flight + timedelta(minutes=time_trip)))
                if(len(task_bus) > 0):
                    continue

                last_task = (task.objects.filter(bus_id = cur_bus_id) & task.objects.filter(time_to__lte = date_cur_flight)).order_by("-time_to")[0]
                next_task = (task.objects.filter(bus_id = cur_bus_id) & task.objects.filter(time_to__gt = date_cur_flight)).order_by("time_to")

                time_to_trip = get_time_trip(last_task.point_to, point_from_id)
                if(len(next_task) > 0):
                    time_from_trip = get_time_trip(point_to_id, next_task[0].point_from)
                    full_time = time_to_trip + time_trip + time_from_trip + time_plus
                    if(next_task[0].time_from < last_task.time_to + timedelta(minutes = full_time)):
                        continue
                else:
                    full_time = time_to_trip + time_trip + time_plus

                cur_bus_capacity = buses.objects.filter(id = cur_bus_id)[0].capacity
                height_bus = full_time * (100 / cur_bus_capacity)
                if height_bus not in best_bus:
                    best_bus[height_bus] = {}
                best_bus[height_bus][last_task.time_to] = [per, full_time, cur_bus_capacity]
                heights_bus.append(full_time * (100 / cur_bus_capacity))
            pas_amount = int(e.passengers_amount)
            heights_bus.sort()
            avail100 = []
            true_bus = []
            for h in heights_bus:
                heights = sorted(list(best_bus[h].keys()), reverse = True)
                for bus in heights:
                    if pas_amount <= 50:
                        if best_bus[h][bus][2] == 50:
                            true_bus.append(best_bus[h][bus][0])
                            pas_amount -= 50
                        else:
                            avail100.append(best_bus[h][bus][0])
                    else:
                        true_bus.append(best_bus[h][bus][0])
                        pas_amount -= best_bus[h][bus][2]
                    if(pas_amount <= 0):
                        break
                if (pas_amount <= 0):
                    break

            if(pas_amount > 0 and len(avail100) > 0):
                true_bus.append(avail100[0])

            for bus in true_bus:
                last_key = task.objects.order_by("-id")[0].id
                new_task = task.objects.create(point_from=point_from_id, point_to=point_to_id,
                                               time_from=date_cur_flight,
                                               time_to=date_cur_flight + timedelta(minutes=time_plus + time_trip),
                                               bus_id=bus.bus_id, flight_id=e.id, id=last_key + 1)




def check_auth(request):
    try:
        resp = None
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

    return resp, role

def logout(request):
    response = render(request, 'html/authRedirect.html', {})
    response.set_cookie('userCode', '' ,max_age = 0)
    return response

def Setting(request):

    t1 = get_template('html/setting.html')
    html1 = t1.render({"host": request.get_host(), 'num': 1})
    return HttpResponse(html1)

def main(request):
    #update()
    auth, role = check_auth(request)
    if auth != None:
        return auth

    if role == 0:
        return redirect('main_admin')
    if role == 1:
        return redirect('driver_main')




    response = render(request, 'html/main.html', {"host": request.get_host()})
    return response

@csrf_exempt
def getTime(request):
    return HttpResponse(getTimeJson(), content_type='application/json')