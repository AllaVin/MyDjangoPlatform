from django.urls import path
from TaskManager_app.views import test, show_new_tasks
from TaskManager_app.views import test
from TaskManager_app.views import show_new_tasks, show_overdue_done_subtasks
urlpatterns = [
    path('task_manager_path', view=test),  # http://127.0.0.1:8000/TaskManager_app/task_manager_path

    path('show_new_tasks/', view=show_new_tasks), # http://127.0.0.1:8000/TaskManager_app/show_new_tasks

    # Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
    path('show_overdue_done_subtasks/', view=show_overdue_done_subtasks), # http://127.0.0.1:8000/TaskManager_app/show_overdue_done_subtasks/
]
