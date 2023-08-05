from django.contrib import admin
from zenflow_workflow.models import Workflow, Task, TaskAssignment, Comment, Link

# Register your models here.
admin.site.register(Workflow)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(Comment)
admin.site.register(Link)