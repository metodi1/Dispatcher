from django.contrib import admin

from dispatcher.routes.models import RoundDetails


@admin.register(RoundDetails)
class RoundDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_point', 'end_point', 'waypoints', 'total_distance', 'created_at']
