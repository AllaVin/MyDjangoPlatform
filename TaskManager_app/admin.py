from django.contrib import admin
from TaskManager_app.models import Task, SubTask, Category, Project

# admin.site.register(Category)
# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Project)

# Register your models here.
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title',
#                     "description",
#                     'get_categories',
#                     'status',
#                     'project',
#                     'priority',
#                     'deadline',
#                     'created_at',)
#     search_fields = ('title',)
#     ordering = ('title',)
#     list_per_page = 5

## ----- Кастомизация отображения Task -----
# чтобы в админке Django в списке задач отображалось сокращённое название,
# но при редактировании — использовалось полное.
# Это классическая задача кастомизации отображения в list_display.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title',
                    'description',
                    'status',
                    'priority',
                    'deadline',
                    'created_at')
    ordering = ('title',)

    def short_title(self, obj): # short_title(self, obj) — метод, который вызывается для каждой строки в таблице.
        return obj.title if len(obj.title) <= 10 else obj.title[:10] + '...'

    short_title.short_description = "Title" ## — это то, что отобразится в заголовке колонки вместо short_title.
                                            ## short_description — это специальное встроенное свойство Django admin,
                                            ## которое задаёт заголовок столбца в админке, если ты используешь метод в list_display.

# @admin.register(SubTask)
# class SubTaskAdmin(admin.ModelAdmin):
#     list_display = ('title',
#                     "description",
#                     'task',
#                     'status',
#                     'deadline',
#                     'created_at',)
#     search_fields = ('title',)
#     ordering = ('title',)
#     list_per_page = 5


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 5

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'description',
                    'created_at',)  # добавь нужные поля
    search_fields = ('name',)


# ##  _____ Добавление настройки инлайн форм для админ класса задач.
# ## При создании задачи должна появиться возможность создавать сразу и подзадачу.
# class SubTaskInline(admin.StackedInline):
#     model = SubTask
#     extra = 2
#
# class TaskAdmin(admin.ModelAdmin):
#     inlines = [SubTaskInline] ## В Publisher встреивается Books. Открываешь Publisher -> можешь редактировать Books
#
# admin.site.register(Task, TaskAdmin)

## _____ Добавление кастомного Action для Подзадач, который поможет выбранные в Админ панели объекты переводить в статус Done

class SubTaskAdmin(admin.ModelAdmin):
    def show_all_done (self, request, queryset):
        queryset.update(status='Done') ## Обратить внимание Done должно быть написать
                                       ## точно так же как в Choices в models.py в левой части
    show_all_done.short_description = "Show all Done"
    actions = [show_all_done]

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    def show_all_done (self, request, queryset):
        queryset.update(status='Done')
    show_all_done.short_description = "Show all Done"
    actions = [show_all_done]