import re
import django
from django.utils.text import wrap
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime, timedelta
from math import log

def get_user_model():
    if django.VERSION[:2] >= (1, 5):
        from django.contrib.auth import get_user_model
        return get_user_model()
    else:
        from django.contrib.auth.models import User
        return User


def get_username_field():
    if django.VERSION[:2] >= (1, 5):
        return get_user_model().USERNAME_FIELD
    else:
        return 'username'

epoch = datetime(1970, 1, 1)

def epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

def hot(likes, date):
    #order = log(max(abs(likes), 1), 10)
    order = log(likes^4)
    seconds = epoch_seconds(date) - 1425253284
    new_score = 10*(order + seconds / 1000000)
    return round(new_score, 7)

