from django.db import models
from django.utils import timezone

class WaterLevel(models.Model):
    distance = models.FloatField(verbose_name="Jarak (cm)", default=0)
    ph_value = models.FloatField(verbose_name="pH", default=7.0)
    tds_value = models.FloatField(verbose_name="TDS (ppm)", default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    # timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Sensor Data"

    def __str__(self):
        return f"Data @ {self.timestamp}"