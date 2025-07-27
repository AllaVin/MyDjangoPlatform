
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.
LANG_CHOICES = [
    ('py', 'Python'),
    ('java', 'Java'),
    ('c#', 'C#'),
]


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    # Описание проекта может быть БОЛЬШИМ, потому TextField
    description = models.TextField(null=True, blank=True)
    # Определение языка проекта
    lang = models.CharField(choices=LANG_CHOICES)
    # created_at = models.DateTimeField(null=True, blank=True)     # default=timezone.now,
    created_at = models.DateTimeField(default=timezone.now)  # default=timezone.now,

    # Метод          Назначение
    # Целевая аудитория
    # Используется в…
    # __repr__  --->  Точное, техническое описание
    # Разработчики
    # repr(obj), интерактивный режим
    # __str__  -->  Красивое, понятное описание
    # Пользователи
    # str(obj), print(obj)
    # https://chatgpt.com/share/6853e1e0-7cc8-8008-a7ea-d5f76e515b23

    class Meta:
        # ordering = ['-name']        # Сортировка по убыванию по имени.
        # verbose_name = 'Project'
        # verbose_name_plural = "Projects"
        # unique_together = (('name', 'description'),)
        # constraints = [
        #     models.CheckConstraint(condition=models.Q(name__icontains='project'), name='project_name__icontains'),
        #     # models.UniqueConstraint(fields=['name', 'language'], name='project_name__language'),
        #     # See links: https://docs.djangoproject.com/en/5.2/ref/models/constraints/
        # ]
        ordering = ['-name']
        verbose_name = 'Project'
        verbose_name_plural = "Projects"
        unique_together = (('name', 'description'),)

    def __str__(self):
        return self.name

TAG_CHOICES = [
    ('Backend', 'Backend'),
    ('Frontend', 'Frontend'),
    ('Q&A', 'Q&A'),
    ('Design', 'Design'),
    ('DevOPS', 'DevOPS'),
]


class Tag(models.Model):
    name = models.CharField(choices=TAG_CHOICES, verbose_name='Tag Name')
    # Описание ТЕГА может быть коротким, потому CharField
    description = models.CharField(max_length=255, verbose_name='Tag Description')
    # Один ТЭГ может быть во многих проектах, и для одного тега может быть много проектов,
    # значит связь - many-to-many:
    projects = models.ManyToManyField('Project', related_name='tags', blank=True)   # projectS - потому что может быть много проектов.
    # task = models.ManyToMany()

    def __str__(self):
        return self.name



GRADE_CHOICES = [
    ('Junior', 'Junior'),
    ('middle', 'Middle'),
    ('senior', 'Senior'),
]

class Developer(models.Model):
    name = models.CharField(max_length=255)
    grade = models.CharField(choices=GRADE_CHOICES, max_length=255) # текущая версия пайтона требует, чтобы везде где используются choices - надо указывать max_length
    project = models.ManyToManyField('Project', related_name='developers', blank=True) # Кода связать

    def __str__(self):
        return self.name

# //////////    TO LES 21 Additional Pract  from 23-06-25    //////////////////////////////////////////////////////////

# Создайте модель Task со следующими полями:
#   - Название задачи: строковое поле, уникальное, минимальная длина названия - 10 символов
#   - Описание: большое строковое поле, может быть пустым
#   - Статус: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных статусов. По умолчанию все задачи новые
#   - Приоритет: строковое поле максимальной длины в 15 символов, должно быть полем выбора разных приоритетов
#   - Проект: связь с моделью Project, при удалении проекта все задачи должны удаляться
#   - Дата создания задачи: поле, поддерживающее и дату, и время, заполняется автоматически только при создании
#   - Дата обновления: поле, поддерживающее и дату, и время, заполняется автоматически всегда
#   - Дата удаления: поле, в котором может ничего не быть

# Расширьте модель Task дополнительным хранением тегов:
#   1) Создайте модель тегов (Tag):
#       - Имя тэга (Строковое поле, уникальное)
#   2) Добавьте поле due_date (срок выполнения) в модель Task.
#   3) Свяжите модель Задачи с тегами через связь “Многие ко многим”, добавив в модель задачи новое поле tags.


STATUS_CHOICES=[
    ('new', 'New'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
    ('closed', 'Closed'),
    ('blocked', 'Blocked'),
    ('pending', 'Pending'),
]

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('very_high', 'Very High'),
]

class Task(models.Model):
    name = models.CharField(validators=[MinLengthValidator(10)], unique=True)
    description = models.TextField(null=True, blank=True)  # null --> for DB, blank --> for Admin.
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES)
    # Связь с моделью Project:
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # To Tag
    due_date = models.DateTimeField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True, default=None)

    # Relation to User:
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='project_tasks', null=True, blank=True)


def __str__(self):
        return self.name


# Настройте отображение моделей Project, Task, Tag в админ-панели. Реализуйте следующие возможности:
#   1) Поиск по названию задачи для модели Task.
#   2) Поиск по названию проекта для модели Project.
#   3) У модели Task в Админ-панели должны отображаться поля:
#       - Название задачи
#       - Проект
#       - Статус
#       - Приоритетность
#       - Дата создания
#       - Дата сдачи задачи (due_date)



# Создайте связь модели пользователя (User) с моделью Task.
# Добавьте связь к модели Task через поле assignee, которое будет ссылаться на пользователя.
# При выборе типа связи учтите, что на одной задаче может быть одновременно только один сотрудник.


# Добавьте нового пользователя и задачи для него. Для этого выполните действия:
#   1) Создайте нового пользователя через Административную панель, добавьте новые задачи и назначьте его на эти задачи.
# enki_nabu / pass Disabled
#   2) Добавьте assignee в список отображаемых полей в Административной панели
#   3) Добавьте в Административную панель возможность фильтрации задач по конкретному assignee.


# Добавьте настройки к модели Project:
# 1) Добавьте порядок отображения всех проектов по их названию в порядке убывания
# 2) Добавьте отображение названия модели Project во множественном и единственном числах
# 3) Добавьте настройку уникальности каждого проекта сразу по нескольким полям (название и описание проекта)