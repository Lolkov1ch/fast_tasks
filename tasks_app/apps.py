from django.apps import AppConfig


class TasksAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_app'
    
    def ready(self):
        import tasks_app.signals

