from django.contrib import admin
from project.models import Tag, Project, Developer, Task


# Сoздание красивого класса Администратора для модели Tag:
class TagAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name',)
    # Задание полей по которым будет производиться поиск
    search_fields = ('name',)


# Создание класса администратора для модели Project
class ProjectAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name', 'created_at')
    # search_fields = ('name',)
    # Задание полей по которым будет производиться поиск
    readonly_fields = ('created_at',)
    search_fields = ('name',)


# Создание класса администратора для модели Developer
class DeveloperAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name', 'grade')
    # Задание полей по которым будет производиться поиск
    search_fields = ('name', 'grade')


    # Сoздание красивого класса Администратора для модели Task:
class TaskAdmin(admin.ModelAdmin):
    # Определение полей, которые будут отображаться в списке объектов модели
    list_display = ('name', 'status', 'priority', 'created_at', 'due_date', 'assignee')  # project__name - для обращения к связанной модели __ .
    # Задание полей по которым будет производиться поиск
    search_fields = ('name',)
    list_filter = ('status', 'priority', 'created_at', 'due_date', 'assignee__username')



    def project_name(self, obj):
        return obj.project.name

    project_name.short_description = 'Project Name'

admin.site.register(Tag, TagAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Task, TaskAdmin)