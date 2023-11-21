from django.apps import AppConfig


class DoctorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctors'
    #change the display name of the app in the admin panel
    verbose_name = 'Setting/Reviews'
