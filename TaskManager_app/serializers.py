from datetime import date
from rest_framework import serializers
from TaskManager_app.models import Task, SubTask, Category


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'project']
        # _____ HW_13 Задание 4: Валидация данных в сериализаторах
        # Создайте TaskCreateSerializer и добавьте валидацию для поля deadline, чтобы дата не могла быть в прошлом.
        # Если дата в прошлом, возвращайте ошибку валидации.
        # _____ Шаги для выполнения:
        # Определите TaskCreateSerializer в файле serializers.py.
        # Переопределите метод validate_deadline для проверки даты.
        def validate_deadline(self, value):
            if value < date.today():
                raise serializers.ValidationError("Deadline не может быть в прошлом.")
            return value


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'project']


class AllTasksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'project']


class TaskByIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'project']


class TaskCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'status']

# _____ HW_13 Задание 1: Переопределение полей сериализатора
# Создайте SubTaskCreateSerializer, в котором поле created_at будет доступно только для чтения (read_only).
# _____ Шаги для выполнения:
# Определите SubTaskCreateSerializer в файле serializers.py.
# Переопределите поле created_at как read_only.
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True) # Такое поле нельзя будет изменить при создании или обновлении объекта через API.
    class Meta:
        model = SubTask
        fields = '__all__'

# _____ HW_13 Задание 2: Переопределение методов create и update
# Создайте сериализатор для категории CategoryCreateSerializer, переопределив методы create и update для проверки уникальности названия категории. Если категория с таким названием уже существует, возвращайте ошибку валидации.
# _____Шаги для выполнения:
# Определите CategoryCreateSerializer в файле serializers.py.
# Переопределите метод create для проверки уникальности названия категории.
# Переопределите метод update для аналогичной проверки при обновлении.
# class CategoryCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'description', 'created_at']
#         read_only_fields = ['created_at']
#
#     def validate_name(self, value):
#         # Проверка уникальности названия (без учёта регистра)
#         existing = Category.objects.filter(name__iexact=value)
#         if self.instance:
#             # При update исключаем текущий объект
#             existing = existing.exclude(pk=self.instance.pk)
#         if existing.exists():
#             raise serializers.ValidationError("Категория с таким названием уже существует.")
#         return value
#
#     def create(self, validated_data):
#         return Category.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         return instance

# _____ HW_13 Задание 3: Использование вложенных сериализаторов
# Создайте сериализатор для TaskDetailSerializer, который включает вложенный сериализатор для полного отображения связанных подзадач (SubTask). Сериализатор должен показывать все подзадачи, связанные с данной задачей.
# _____ Шаги для выполнения:
# Определите TaskDetailSerializer в файле serializers.py.
# Вложите SubTaskSerializer внутрь TaskDetailSerializer.
class SubTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'is_completed', 'created_at']

class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'project', 'subtasks']

# HW_16 Task 1. Реализация CRUD для категорий с использованием ModelViewSet, мягкое удаление.
# Реализовать полный CRUD для модели категорий (Categories) с помощью ModelViewSet, добавить кастомный метод для подсчета количества задач в каждой категории. Реализовать систему мягкого удаления для категорий.
# Задание 1: Реализация CRUD для категорий с использованием ModelViewSet
# Шаги для выполнения:
# Создайте CategoryViewSet, используя ModelViewSet для CRUD операций.
# Добавьте маршрут для CategoryViewSet.
# Добавьте кастомный метод count_tasks используя декоратор @action для подсчета количества задач, связанных с каждой категорией.
class CategorySerializer(serializers.ModelSerializer): # Для чтения
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_deleted', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_deleted']
        ref_name = "TaskManagerApp_CategorySerializer"

class CategoryCreateUpdateSerializer(serializers.ModelSerializer): # Для создания и редактирования
    class Meta:
        model = Category
        fields = ['name']
        ref_name = "TaskManagerApp_CategoryCreateUpdateSerializer"

