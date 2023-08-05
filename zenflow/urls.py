"""zenflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from schedule.views import CalendarView

from django.conf import settings
from django.conf.urls.static import static
from zenflow_userinfo import urls
from zenflow_userinfo import views
from zenflow_workflow import views
from django.conf.urls import include



urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index, name='index'),
    path('', include('zenflow_authentication.urls')),
    path('userinfo/', include('zenflow_userinfo.urls')),
    path('workflow/', include('zenflow_workflow.urls')),
    # path('calendar/', CalendarView.as_view(), name='calendar'),
    # path('event/<int:pk>/', EventEditView.as_view(), name='event_edit'),
    # path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
