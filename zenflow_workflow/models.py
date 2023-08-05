from django.db import models
from zenflow_userinfo.models import Team, Employee
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Workflow(models.Model):
    workflow_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=1000)
    date_started = models.DateField()
    date_completed = models.DateField(null=True, blank=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, related_name='workflows')

class Task(models.Model):
    STATUS_CHOICES = ( ('to do','TO DO') , ('in progress','IN PROGRESS') , ('in review','IN REVIEW') , ('completed','COMPLETED'))
    task_id = models.AutoField(primary_key=True)
    workflow_id = models.ForeignKey(Workflow, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='To Do')
    deadline = models.DateField()


class TaskAssignment(models.Model):
    unique_together = (('task_id', 'employee_id'),)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=100)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='images/', default='images/default.jpg')

class Link(models.Model):
    link_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2048)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)