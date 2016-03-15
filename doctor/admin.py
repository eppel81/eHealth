from django.contrib import admin

import models


@admin.register(models.Doctor)
class AdminDoctor(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'gender', 'timezone',
                    'photo', 'phone_appointment', 'video_appointment')
    filter_horizontal = ('languages', )


@admin.register(models.DoctorPayment)
class AdminDoctorPayment(admin.ModelAdmin):
    list_display = ('doctor', 'name', 'tax_id', 'bill', 'iban', 'hold')


@admin.register(models.DoctorHistory)
class AdminDoctorHistory(admin.ModelAdmin):
    list_display = ('doctor', 'record_date', 'type')


@admin.register(models.DoctorPaymentHistory)
class AdminDoctorPaymentHistory(admin.ModelAdmin):
    list_display = ('doctor', 'record_date', 'payment', 'money')


@admin.register(models.DoctorSpecialty)
class AdminDoctorSpecialty(admin.ModelAdmin):
    list_display = ('doctor', 'specialty', 'primary')


@admin.register(models.DoctorWorkExperience)
class AdminDoctorWorkExperience(admin.ModelAdmin):
    list_display = ('doctor', 'care_facility', 'position', 
                    'start_date', 'end_date')


@admin.register(models.DoctorAppointmentTime)
class AdminDoctorAppointmentTime(admin.ModelAdmin):
    list_display = ('start_time', 'duration', 'free')
