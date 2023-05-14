from django.apps import AppConfig


class AppUserlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'App_Userlog'
    
    def ready(self):
        import App_Userlog.signals
