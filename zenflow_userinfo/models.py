from django.db import models
from PIL import Image
from io import BytesIO

# Create your models here.

class Team(models.Model):
    team_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    birth_date = models.DateField()
    email = models.CharField(max_length = 320)
    password = models.CharField(max_length = 256)
    phone_number = models.CharField(max_length = 12)
    is_manager = models.BooleanField()
    team_id = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='employees', null=True, blank=True)
    profile_picture = models.CharField(max_length = 256, default='/static/images/default.jpg')

    def __str__(self):
        return self.last_name