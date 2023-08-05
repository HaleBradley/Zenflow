from django.urls import path
from zenflow_workflow import views

urlpatterns = [
    path('createworkflow/', views.createworkflow, name='createworkflow'),
    path('backlog/', views.backlog, name='backlog'),
    path('worklist/', views.work_list, name='worklist'),
    path('<int:pk>save/', views.workflow_save, name='workflowsave'),
    path('<int:pk>tasksave/', views.task_save, name='tasksave'),
    path('workflowview/', views.workflow_view, name='workflowview'),
    path('<int:pk>edit/', views.editworkflow, name='editworkflow'),
    path('delete-work/<int:pk>', views.deleteWorkflow, name='deletework'),
    path('addlink/', views.addlink, name='addlink'),
    path('addcomment/', views.addcomment, name='addcomment'),
    path('addtask/', views.addtask, name='addtask'),
    path('complete/', views.complete_workflow, name='complete'),
    path('edit/', views.edittask, name='edittask')
]

