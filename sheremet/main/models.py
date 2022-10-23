from django.db import models

# Create your models here.
class setting(models.Model):
    UTC = models.SmallIntegerField(default = 0, blank=True)

class flights(models.Model):
    date = models.DateField(blank=True, null=True)
    arr_dep = models.CharField(max_length=1, blank=True, null=True)
    terminal = models.CharField(max_length=1, blank=True, null=True)
    code_ak = models.CharField(max_length=5, blank=True, null=True)
    flight_number = models.CharField(max_length=10, blank=True, null=True)
    planned_time = models.TimeField(blank=True, null=True)
    code_ap = models.CharField(max_length=5, blank=True, null=True)
    airport = models.CharField(max_length=20, blank=True, null=True)
    plane_type = models.CharField(max_length=5, blank=True, null=True)
    parking_place_number = models.CharField(max_length=4, blank=True, null=True)
    gate_number = models.CharField(max_length=15, blank=True, null=True)
    passengers_amount = models.CharField(max_length=4, blank=True, null=True)

class points(models.Model):
    point_id = models.IntegerField(blank=True, null=True)
    location_id = models.CharField(max_length=15, blank=True, null=True)

class roads(models.Model):
    source_point_id = models.IntegerField(blank=True, null=True)
    target_point_id = models.IntegerField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)

class bus_drivers(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    status_id = models.IntegerField(blank=True, null=True)

class buses(models.Model):
    capacity = models.IntegerField(blank=True, null=True)
    trip_without_refueling = models.IntegerField(blank=True, null=True)
    auto_task = models.BooleanField(blank=True, null=True)

class task(models.Model):
    bus_id = models.IntegerField(blank=True, null=True)
    point_from = models.IntegerField(blank=True, null=True)
    point_to = models.IntegerField(blank=True, null=True)
    time_from = models.DateTimeField(blank=True, null=True)
    time_to = models.DateTimeField(blank=True, null=True)
    flight_id = models.IntegerField(blank=True, null=True)

class working_period(models.Model):
    from_period = models.DateTimeField(blank=True, null=True)
    to_period = models.DateTimeField(blank=True, null=True)
    bus_driver_id = models.IntegerField(blank=True, null=True)
    bus_id = models.IntegerField(blank=True, null=True)