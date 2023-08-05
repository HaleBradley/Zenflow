from django.urls import path
from zenflow_userinfo import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('teamlist/', views.teamlist, name='teamlist'),
    path('emplist/', views.emplist, name='emplist'),
    path('teamcreate/', views.createteam, name='teamcreate'),
    path('delete-team/<int:team_id>/', views.deleteTeam, name='delete_team'),
    path('<int:pk>editteam/', views.editTeam, name='editteam'),
    path('deleteaccount/', views.deleteaccount, name='deleteaccount'),
    path('editaccount/', views.editaccount, name='editaccount'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('canceledit/', views.canceledit, name='canceledit')
]
