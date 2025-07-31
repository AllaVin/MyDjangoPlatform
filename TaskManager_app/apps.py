from django.apps import AppConfig


class TaskmanagerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TaskManager_app'

    def ready(self):
        import TaskManager_app.signals