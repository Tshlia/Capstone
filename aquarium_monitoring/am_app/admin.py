from django.contrib import admin
from .models import WaterLevel

@admin.register(WaterLevel)
class WaterLevelAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'distance', 'ph_value', 'tds_value')
    list_filter = ('timestamp',)
    search_fields = ('timestamp',)