from django.contrib import admin

from utils.models import *


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(TimeZone)
class AdminTimeZone(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Country)
class AdminCountry(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('timezone',)


@admin.register(Specialty)
class AdminSpecialty(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Language)
class AdminLanguage(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ActivityType)
class AdminActivityType(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AppointmentSchedule)
class AdminAppointmentSchedule(admin.ModelAdmin):
    list_display = (
        'doctor', 'date', 'day_shift', 'day_from', 'day_to', 'night_shift',
        'night_from', 'night_to')


@admin.register(SupportUser)
class AdminSupportUser(admin.ModelAdmin):
    pass
    # list_display = ('name', res)