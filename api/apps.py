from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'MyUs'
