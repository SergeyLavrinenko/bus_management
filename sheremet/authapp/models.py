from django.db import models

# Create your models here.
# Create your models here.
#

class users(models.Model):
    name = models.CharField(max_length = 20)
    login = models.CharField(max_length = 20)
    password = models.CharField(max_length = 60)
    code = models.CharField(max_length = 40)
    role = models.SmallIntegerField(default = 0, blank=True)
    last_date = models.DateTimeField(blank=True, null=True)
    is_admin = models.BooleanField(default=False, null=True)