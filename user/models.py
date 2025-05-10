from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    theme_color = models.CharField(max_length=20, default="#A8D5BA")
