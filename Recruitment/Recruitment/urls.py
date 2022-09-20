"""Recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path, include
from RecruitmentApp import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Recruitment Pipeline API",
        default_version='v1',
        description="The below API's are for creating new job listings, creating new applicant profiles & managing applications.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)




urlpatterns = [
    
    path('recruit/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('Applicants/', views.ApplicantList.as_view()),
    path('Job/', views.JobList.as_view()),
    path('Applications/', views.ApplicationList.as_view()),
    path('Applications/<int:pk>', views.ApplicationDetails.as_view())
]
    


