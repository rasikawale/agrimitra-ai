from django.contrib import admin
from .models import Farmer, Farm


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'mobile',
        'village',
        'district',
        'state',
        'created_at',
    )

    search_fields = (
        'name',
        'mobile',
        'village',
        'district',
    )


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'farm_name',
        'farmer',
        'location',
        'area',
        'soil_type',
        'created_at',
    )

    search_fields = (
        'farm_name',
        'location',
        'soil_type',
        'farmer__name',
    )