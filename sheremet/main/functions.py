from main.models import setting
from django.utils import timezone
from datetime import datetime, timedelta
import json


def getTimeJson() -> object:
    config = setting.objects.all()[0]
    time = (timezone.now() + timedelta(hours=config.UTC)).strftime("%H:%M")
    dump = json.dumps({"time": time})

    return dump