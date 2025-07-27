from django.contrib.auth.models import User
from django.db import models

from TaskManager_app.permissions import IsAdminOrOwner

STATUS_CHOICES = [
    ('New', 'New'),
    ('In_Progress', 'In_Progress'),
    ('Pending', 'Pending'),
    ('Blocked', 'Blocked'),
    ('Done', 'Done'),
]

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ автоматически при создании
    updated_at = models.DateTimeField(auto_now=True)  # ✅ при каждом изменении
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'TaskManager_app_category'
        verbose_name_plural = 'Category'
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_category_name'),
        ]

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='tasks') # M2M
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Low')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', null=True)

    class Meta:
        db_table = 'TaskManager_app_task'  # Задаем имя таблицы в базе данных
        ordering = ['-created_at']  # Сортировка по убыванию даты публикации
        verbose_name = 'Task'  # Человекочитаемое имя модели
        # verbose_name_plural = 'fiction books'  # Человекочитаемое множественное число имени модели
        # unique_together = ('title', 'category')  # Уникальность по комбинации полей title и category
        # get_latest_by = 'created_at' # Поле для определения последней записи в таблице
        # indexes = [
        #     models.Index(fields=['title', 'status']),
        #     models.Index(fields=['created_at'], name='created_at_idx'),
        # ] # Создание различных индексов
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_project_title'),
        ]

    def __str__(self):
        return f'{self.title}'

    def get_categories(self):
        return ", ".join([c.name for c in self.categories.all()])

    get_categories.short_description = "Categories"  # для красивой подписи в админке

class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')  #  O2M
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'TaskManager_app_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        constraints = [
            models.UniqueConstraint(fields=['title'], name='unique_subtask_title')
        ]

    def __str__(self):
        return f"{self.title}"



