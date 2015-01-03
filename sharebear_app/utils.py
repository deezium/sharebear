import re
import django
from django.utils.text import wrap
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail

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
