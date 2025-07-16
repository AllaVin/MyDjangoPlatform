from datetime import timedelta
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from TaskManager_app.models import Task, Project, SubTask
from TaskManager_app.serializers import TaskCreateSerializer, AllTasksListSerializer, TaskByIDSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Count
from django.utils.timezone import now

# _____ Задание 5 HW_13: Создание классов представлений
# Создайте классы представлений для работы с подзадачами (SubTasks), включая создание, получение, обновление и
# удаление подзадач. Используйте классы представлений (APIView) для реализации этого функционала.
# ______ Шаги для выполнения:
# Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
# Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).
# Добавьте маршруты в файле urls.py, чтобы использовать эти классы.
from rest_framework.views import APIView
from TaskManager_app.serializers import SubTaskCreateSerializer
from TaskManager_app.models import SubTask



# # _____ Задание 1 HW_12: Эндпоинт для создания задачи
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

# # _____ Task 2 HW_12. Эндпоинты для получения списка задач и конкретной задачи по её ID
    # Создайте два новых эндпоинта для:
    # Получения списка задач
    # Получения конкретной задачи по её уникальному ID
    #   Шаги для выполнения:
    # Создайте представления для получения списка задач и конкретной задачи.
    # Создайте маршруты для обращения к представлениям.

# # _____ Task1 HW_12 Список всех задач
@api_view(['GET'])
def all_tasks_list(request):
    tasks = Task.objects.all()
    serializer = AllTasksListSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# # _____ Task 2 HW_12. Задача по ID
@api_view(['GET'])
def view_task_by_id(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskByIDSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)

# # _____ Task 3 HW_12. Агрегирующий эндпоинт для статистики задач
        # Создайте эндпоинт для получения статистики задач, таких как общее количество задач, количество задач по каждому статусу и количество просроченных задач.
        # Шаги для выполнения:
        # Определите представление для агрегирования данных о задачах.
        # Создайте маршрут для обращения к представлению.
        # Оформите ваш ответ следующим образом:
        # Код эндпоинтов: Вставьте весь код представлений и маршрутов.
        # Скриншоты ручного тестирования: Приложите скриншоты консоли или Postman, подтверждающие успешное выполнение запросов для каждого эндпоинта.

# # # ____ Task 3.1 Общее количество задач
@api_view(['GET'])
def task_count(request):
    count = Task.objects.count()
    return Response({'total_tasks': count}, status=status.HTTP_200_OK)

# # ____ Task 3.2 Количество задач по каждому статусу
@api_view(['GET'])
def task_per_status(request):
    tasks_per_status = Task.objects.values('status').annotate(count=Count('status'))
    # Преобразуем в формат {"New": 5, "Done": 3, ...}
    result = {item['status']: item['count'] for item in tasks_per_status}
    return Response(result, status=status.HTTP_200_OK)

# # ____ Task 3.3 Количество просроченных задач
@api_view(['GET'])
def overdue_tasks_count(request):
    today = now().date()
    # считаем задачи, у которых deadline в прошлом и статус не "Done"
    count = Task.objects.filter(deadline__lt=today).exclude(status='Done').count()
    return Response({'overdue_tasks': count}, status=status.HTTP_200_OK)



# # ____ Other tasks from others HW

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
    # return HttpResponse("Congrats, Task and SubTask have been created!")
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


# _____ HW_13 Task5. Класс для создания и просмотра списка подзадач
class SubTaskListCreateView(APIView):
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# _____ HW_13 Task5. Класс для получения, обновления и удаления подзадачи по ID
class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return None

    def get(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if not subtask:
            return Response({'error': 'SubTask not found'}, status=status.HTTP_404_NOT_FOUND)
        subtask.delete()
        return Response({'message': 'SubTask deleted'}, status=status.HTTP_204_NO_CONTENT)
