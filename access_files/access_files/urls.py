"""access_files URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from file_system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health_check/', views.HealthCheckView.as_view()),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    path('project/',views.ProjectsView.as_view()),
    path('assign/project/<int:project_id>/', views.AssignProjectView.as_view()),
    path('project/<int:project_id>/files', views.ProjectFilesView.as_view()),
    path('project/<int:project_id>/publish_file', views.PublishFilesView.as_view()),
]
