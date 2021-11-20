from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user_id = models.CharField(max_length=12, unique=True)
    user_name = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=200, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class PayInfo(models.Model):
    card_id = models.IntegerField(primary_key=True)
    card_no = models.CharField(max_length=16, unique=True)
    security_code = models.CharField(max_length=3)
    valid_date1 = models.DateField()
    valid_date2 = models.DateField()
    user_id = models.ManyToManyField(UserProfile)
    is_active = models.BooleanField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
