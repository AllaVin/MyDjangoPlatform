from django.urls import path, include
from TaskManager_app.serializers import AllTasksListSerializer
from TaskManager_app.views import new_task
from TaskManager_app.views import all_tasks_list
from TaskManager_app.views import view_task_by_id
from TaskManager_app.views import task_count
from TaskManager_app.views import task_per_status
from TaskManager_app.views import overdue_tasks_count
from TaskManager_app.views import SubTaskDetailUpdateDeleteView, SubTaskListCreateView


# from TaskManager_app.views import test, show_new_tasks
# from TaskManager_app.views import test
# from TaskManager_app.views import show_new_tasks, show_overdue_done_subtasks
urlpatterns = [
    # path('task_manager_path', view=test),  # http://127.0.0.1:8000/TaskManager_app/task_manager_path

    # path('show_new_tasks/', view=show_new_tasks), # http://127.0.0.1:8000/TaskManager_app/show_new_tasks

    # Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
    # path('show_overdue_done_subtasks/', view=show_overdue_done_subtasks), # http://127.0.0.1:8000/TaskManager_app/show_overdue_done_subtasks/
    path('new_task/', view=new_task),  # http://127..0.0.1:8000/TaskManager_app/new_task/
    path('all_tasks_list/', view=all_tasks_list), # http://127..0.0.1:8000/TaskManager_app/all_tasks_list/
    path('view_task_by_id/<int:task_id>/', view=view_task_by_id),  # http://127..0.0.1:8000/TaskManager_app/view_task_by_id/

    path('task_count/', view=task_count), # http://127.0.0.1:8000/TaskManager_app/task_count/
    path('task_per_status/', view=task_per_status), # http://127.0.0.1:8000/TaskManager_app/tasks_per_status/
    path('overdue_tasks_count/', view=overdue_tasks_count), # http://127.0.0.1:8000/TaskManager_app/overdue_tasks_count/

    # HW_13 Task 5. Добавляем маршруты
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
]
