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
    filter_horizontal = ('timezone', )


@admin.register(Specialty)
class AdminSpecialty(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Language)
class AdminLanguage(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AppointmentReason)
class AdminAppointmentReason(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ActivityType)
class AdminActivityType(admin.ModelAdmin):
    list_display = ('name',)






