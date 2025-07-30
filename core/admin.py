from django.contrib import admin
from .models import *

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    search_fields = ('name',)
    list_filter = ('is_popular',)

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active')
    search_fields = ('name', 'phone')
    list_filter = ('is_active', 'services')
    filter_horizontal = ('services',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'status', 'appointment_date')
    search_fields = ('client_name', 'phone')
    list_filter = ('status', 'master', 'services')
    date_hierarchy = 'appointment_date'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'master', 'is_published', 'created_at')
    search_fields = ('client_name', 'text')
    list_filter = ('rating', 'is_published', 'master')
    date_hierarchy = 'created_at'