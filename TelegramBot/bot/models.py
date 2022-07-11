from django.db import models


class User(models.Model):
    phone = models.CharField('Phone number', max_length=50, blank=True)
    username = models.CharField('Username', max_length=150)
    user_id = models.IntegerField('User ID', primary_key=True)
