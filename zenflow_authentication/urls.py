from django.urls import path
from zenflow_authentication import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('helpme/', views.helpme, name='help'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register')
]
