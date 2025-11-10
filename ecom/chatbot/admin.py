from django.contrib import admin
from .models import HealthRecord

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'disease',
        'blood_sugar',
        'blood_pressure_sys',
        'blood_pressure_dia',
        'heart_rate',
        'bmi',
        'created_at',
    )
    list_filter = ('disease', 'created_at')
    search_fields = (
        'disease',
        'blood_sugar',
        'blood_pressure_sys',
        'blood_pressure_dia',
        'heart_rate',
        'bmi',
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ("Patient Health Data", {
            "fields": (
                "disease",
                "blood_sugar",
                "blood_pressure_sys",
                "blood_pressure_dia",
                "heart_rate",
                "bmi",
            )
        }),
        ("System Info", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ('created_at',)
