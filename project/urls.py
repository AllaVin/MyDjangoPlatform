# from project.views import test
from django.urls import path
from django.urls import path, include
from project.views import list_project, list_tasks
from . import views


urlpatterns = [
    # path('admin/', view=test), # http://127.0.0.1:8000/admin/
    # path('test', view=test), # http://127.0.0.1:8000/project/my_path
    path('projects', view=list_project), # http://127.0.0.1:8000/project/projects ## Выведет в JSON формате
    path('tasks', view=list_tasks),  # http://127.0.0.1:8000/project/tasks ## Выведет в JSON формате
    # path('project/admin/', view=test) ## http://127.0.0.1:8000/project/admin/

]