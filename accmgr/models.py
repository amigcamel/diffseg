from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Customized user profile."""

    user = models.OneToOneField(User, unique=True)
    username = models.CharField(max_length=50)
    displayname = models.CharField(max_length=50)
    email = models.EmailField(null=True)
    regtime = models.DateField(default=datetime.now)
    ip = models.CharField(max_length=20)
