"""
URL configuration for DjangoProject_Library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
# from project.views import test
from django.urls import path
from django.contrib import admin


urlpatterns = [
    path("admin/", admin.site.urls), ## http://127.0.0.1:8000/admin/
    # path("project/", project.urls),
    path('project/', include('project.urls')), ## http://127.0.0.1:8000/admin/project/
    path('library/', include('library.urls')), ## http://127.0.0.1:8000/admin/library/
    path('TaskManager_app/', include('TaskManager_app.urls')),
]

