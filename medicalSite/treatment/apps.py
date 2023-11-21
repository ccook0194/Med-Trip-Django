from tabnanny import verbose
from django.apps import AppConfig


class TreatmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'treatment'
    verbose_name = 'Leads & Reviews'
    show_model_count = True