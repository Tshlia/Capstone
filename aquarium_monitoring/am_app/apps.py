# from django.apps import AppConfig


# class AmAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'am_app'

#     def ready(self):
#         if not hasattr(self, 'already_started'):
#             self.already_started = True
#             from .mqtt_client import start_mqtt_client
#             start_mqtt_client()

from django.apps import AppConfig

class AmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'am_app'

    def ready(self):
        if not hasattr(self, 'mqtt_started'):
            from .mqtt_client import start
            start()
            self.mqtt_started = True

# import sys
# from django.apps import AppConfig

# class AmAppConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'am_app'

#     def ready(self):
#         # Pastikan MQTT client hanya mulai saat menjalankan runserver
#         if 'runserver' in sys.argv:
#             try:
#                 from .mqtt_client import start_mqtt_client
#                 start_mqtt_client()
#             except Exception as e:
#                 print(f"[MQTT Init] Error starting MQTT client: {e}")
