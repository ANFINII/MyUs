from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig

class MyUsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myus'
    verbose_name = 'MyUs'
