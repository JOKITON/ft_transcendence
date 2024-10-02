from django.apps import AppConfig


class AutenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'key_app'

class UsermodelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'UserModel'

