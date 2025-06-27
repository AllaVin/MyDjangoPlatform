from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from TaskManager_app.models import Task, Project, SubTask
from TaskManager_app.serializers import TaskCreateSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# ___ HW_12. Задание 1: Эндпоинт для создания задачи
# Создайте эндпоинт для создания новой задачи. Задача должна быть создана с полями title, description, status, и deadline.
# Шаги для выполнения:
# Определите сериализатор для модели Task.
# Создайте представление для создания задачи.
# Создайте маршрут для обращения к представлению.


@api_view(['POST'])
def new_task(request):
    serializer = TaskCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#
# def test(request):
#     # print("🔍 test() was triggered")
#     return HttpResponse("🧪 Test endpoint is alive!")
#
# # ----- CREATING -----
#
#     # Найдём или создадим проект
#     today = timezone.now()
#     project, _ = Project.objects.get_or_create(name="Entertainment")
#     # Нижнее подчеркивание «_» Функция get_or_create(...) возвращает кортеж из двух значений: python
#     # CopyEdit (instance, created) = Model.objects.get_or_create(...) *instance — объект из базы данных(либо
#     # найденный, либо созданный), *created — True, если объект был создан, и False, если был найден.
#
#     # Создаём экземпляр задачи Task (ещё не сохраняем)
#     new_task = Task(
#         title="Prepare presentation",
#         description="Prepare materials and slides for the presentation",
#         status="New",
#         deadline="2025-06-22",
#         project=project
#     )
#     # Вариант с последовательным изменение перед сохранением
#     new_task.title = "Presentation Preparation"  # Переименовали
#     # Сохраняем в базу
#     new_task.save()
#
#
#     # Ищем или создаём другую задачу для SubTask
#     task, created = Task.objects.get_or_create(
#         title="Main Task for Subtask",
#         defaults={
#             "description": "Main task that will own a subtask",
#             "status": "New",
#             "deadline": "2025-06-28",
#             "project": project
#         }
#     )
#
#     # Создаём подзадачу SubTask (ещё не сохраняем)
#     new_subtask = SubTask(
#         title="Research topic",
#         description="Find articles and videos about the topic",
#         status="New",
#         deadline="2025-06-25",
#         task=task
#     )
#     # Вносим изменения при необходимости
#     new_subtask.title = "Find useful resources"
#
#     # Сохраняем в базу
#     new_subtask.save()
#
#
#     # Создаем SubTask с Title "Create slides".
#     # Но сначала нам надо получить Task, к которому он будет относиться
#     task, created = Task.objects.get_or_create(
#         title="Prepare presentation",
#         defaults={
#             "description": "Prepare materials and slides for the presentation",
#             "status": "New",
#             "deadline": today + timedelta(days=3),
#             "project": project
#         }
#     )
#     # Создаём SubTask
#     new_subtask, created = SubTask.objects.get_or_create(
#         title="Create slides",
#         task=task,
#         defaults={
#             "description": "Create presentation slides",
#             "status": "New",
#             "deadline": today + timedelta(days=1),
#         }
#     )
#
#     return HttpResponse("Congrats, Task and SubTask have been created!")
#
# # ----- READING -----
# # Вывести все задачи, у которых статус "New".
# def show_new_tasks(request):
#     tasks = Task.objects.filter(status="New")
#     task_list = ", ".join([task.title for task in tasks])
#     return HttpResponse(f"New tasks: {task_list}")
#
# # Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.
# def show_overdue_done_subtasks(request):
#     now = timezone.now()
#     show_overdue_done_subtasks = SubTask.objects.filter(
#         Q(status="Done") & Q(deadline__lt=now)
#     )
#     subtask_list = ", ".join([subtask.title for subtask in show_overdue_done_subtasks])
#     return HttpResponse(f"Overdue 'Done' SubTasks: {subtask_list}")


# # ----- UPDATING -----
# # Измените статус "Prepare presentation" на "In progress".
# task_update_status = Task.objects.filter(title__iexact="Prepare presentation").update(status='In_Progress') # Независит от регистра
# print(task_update_status)
#
# # Измените срок выполнения для "Gather information" на два дня назад.
# day = timezone.now()
# subtask_update_deadline = SubTask.objects.filter(title__iexact="Gather information").update(deadline=day-timedelta(days=2))
# print(subtask_update_deadline)
#
# # Изменяем описание для "Create slides" на "Create and format presentation slides".
# subtask_update_description = SubTask.objects.filter(title__iexact="Create slides").update(description="Create and format presentation slides")
#
# # ----- DELETING -----
# task_to_delete = Task.objects.get(title="Prepare presentation")
# task_to_delete.delete()

