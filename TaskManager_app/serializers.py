from rest_framework import serializers
from TaskManager_app.models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'project']


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

