from project.views import test
from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', view=test), # http://127.0.0.1:8000/admin/
    path('my_path', view=test), # http://127.0.0.1:8000/project/my_path
    path('project/admin/', view=test) ## http://127.0.0.1:8000/project/admin/
]