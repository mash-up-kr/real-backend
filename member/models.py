from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField('nickname', max_length=50)
    email = models.EmailField('email', unique=True)

