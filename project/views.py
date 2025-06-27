from itertools import count
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.http import HttpResponse
from rest_framework import status
from  project.models import Project, Task
from django.shortcuts import render
from django.db.models import F, Value, Count, Avg
from django.utils import timezone
from django.db.models.functions import ExtractWeekDay
# from colorama import init, Fore, Back, Style
from rest_framework.decorators import api_view
from project.serializers import ProjectListSerializer, TaskListSerializer
from rest_framework.response import Response


# Create your views here.

# ___ 26.06.2025 Task11: Первый сериализатор
@api_view(['GET'])
def list_project(request):
    projects = Project.objects.all()
    if projects.exists():
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# ___ 26.06.2025 Task12: Сериализатор для модели Task
@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all()
    if tasks.exists():
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



# def test(request):
    # ____ ДОБАВЛЕНИЕ НОВОГО проекта:
    # new_project = Project.objects.create(name='New_Project', language='c++')    # тут c++ - с МАЛЕНЬКОЙ буквы.
    # new_project.save()  # СОХРАНИТЬ новый проект

    # ____ УДАЛЕНИЕ ненужного объекта:
    # del_projects = Project.objects.filter(id__gte=6)
    # del_projects.delete()

    # ____ Можно СРАЗУ вызвать Project и СОЗДАТЬ ЭКЗЕМПЛЯР класса:
    # Project.objects.create(name='5th Project', description='This is a description', language='Python')

    # ____ МАССОВОЕ Добавление проектов в БД:
    # project_1 = Project(name='ABC', description='hohoh', language='c')
    # project_2 = Project(name='xyz', description='Coordinates', language='py')
    # project_3 = Project(name='Beautiful Day', language='java')
    # projects = [project_1, project_2, project_3]
    # Project.objects.bulk_create(projects)

    # ____ МАССОВОЕ Обновление поля (language) для ВСЕХ проектов в БД:
    # data_projects = Project.objects.all()
    # for project in data_projects:
    #     # if project.language == 'py':
    #     #     project.language = 'java'
    #     project.language='py'
    # Project.objects.bulk_update(data_projects, ['language'])

    # ____ Обновление имен проектов с добавлением к имени языка, на котором он разрабатывается.
    # Project.objects.update(name=F('name') + F('language'))
    # Project.objects.update(name=Concat(F('name'), Value(' '), F('language')))

    # Project.objects.update(name=Concat(F('name'), Value(' '), F('lang')))

    # #____ 27.06.2025. Task 1.
        # 1. Импортируйте модель Project.
        # 2. Импортируйте модуль timezone из django.
        # 3. Напишите запрос, который выдаст только те проекты, которые были созданы в текущем месяце (месяц брать от даты текущего дня).
        # 4. Если есть хоть один проект - выведите информацию:
        #     ● Название проекта
        #     ● Полная дата его создания


    # projects = Project.objects.filter(created_at__gte="2025-06-25")
    # print(projects)

    # for project in projects:
    #     print(f' 🔎 Project name is {project.name} and it was created at {project.created_at}')
    # print(f'The number of projects is {projects.count()}')


    # # ____ Задача 2. Файлы проектов в день недели
        # 1. Импортируйте модель ProjectFile.
        # 2. Импортируйте класс ExtractWeekDay из django.
        # 3. Напишите запрос, который будет получать список файлов за определённый день, например понедельник:
        # ● Для выборки конкретного значения по полю даты создания используйте класс ExtractWeekDay
        # ● Для упрощения работы с таким значением задайте для него новое, не заявленное в модели поле, например weekday.
        # ● Проведите фильтрацию по этому новому полю.
    # annotated_projects = Project.objects.annotate(week_day=ExtractWeekDay('created_at'))
    # project_per_day = annotated_projects.filter(week_day = 2) # Проекты созданные в Monday
    # for n, project in enumerate(project_per_day, start=1):
    #     print(f'{n} - Project title is "{project.name}"')


    # # ___ Task 3. Общее количество проектов
        # 1. Импортируйте модель Project.
        # 2. Напишите запрос, который будет считать количество всех проектов, которые есть в базе данных.
        # 3. Выведите количество всех проектов в консоль.
    # print(f'The total number of projects is {Project.objects.all().count()}')


    # # ____ Task 5. Среднее количество задач на каждом проекте
        # 1. Импортируйте модель Project.
        # 2. Импортируйте класс AVG из django.
        # 3. Напишите запрос, который сможет для каждого проекта выведите среднее количество задач.
        # 4. Выведите полученные данные.
    # projects = Project.objects.all()
    # for project in projects:
    #     task_count = project.tasks.aggregate(count=Count('id'), average_count=Avg('id'))
    #     print(f"Project: {project} -> number of tasks: {task_count['count']}, average number of tasks: {task_count['average_count']}")
    #

    # # ____ Task 6. Количество задач для каждого пользователя
        # 1. Импортируйте модель User из django.
        # 2. Импортируйте класс Count из django.
        # 3. Напишите запрос, который получит из базы данных количество задач для каждого пользователя.
        # 4. В запросе укажите, что хотим работать только с конкретными полями: ● Username ● Наше собственно созданное поле count_of_tasks
        # 5. Выведите как результат никнейм разработчика и количество прикреплённых за ним задач.

    # annotated_users = User.objects.annotate(number_of_tasks=Count('tasks__id')).values_list('username', 'number_of_tasks')
    # for user in annotated_users:
    #     print(f"User {user[0]} has following number of tasks: {user[1]}")



    # # ____ Импортируйте модель Task.
        # Напишите запрос, который сможет отсортировать все задачи по нескольким полям:
        # - приоритет
        # - дедлайн
        # Выведите название задачи, приоритет и дату завершения.
    # tasks = Task.objects.all().order_by('priority', 'due_date')
    # for task in tasks:
    #     print(f"Tasks title is: {task.name}, has priority: {task.priority} and has dead line at: {task.due_date}")


    # # ____ Сортировка пользователей по количеству задач
    #
    # annot_users = User.objects.all().annotate(tasks_number=Count('tasks__id'))
    # ordered_users = annot_users.order_by('-tasks_number').values_list('username', 'tasks_number')
    # for user in ordered_users:
    #     print(f" For {user[0]} NUMBER of tasks is {user[1]}")


    # # ____ Пагинация для задач
    # all_tasks = Task.objects.all()
    # paginator = Paginator(all_tasks, 2)
    # tasks_per_page = paginator.get_page(2)
    # for tasks in tasks_per_page:
    #     print(f"{'':-<60}")
    #     print(f'Tasks: {tasks}, priority: {tasks.priority}, due date: {tasks.due_date} ')
    #


    # return HttpResponse("Congrats, you are in Project applications!")

