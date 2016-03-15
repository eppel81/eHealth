from django.contrib import admin

import models


@admin.register(models.Patient)
class AdminPatient(admin.ModelAdmin):
    list_display = ('user', 'country', 'timezone', 'photo',
                    'height_ft', 'height_in', 'weight', 'health_complete',
                    'lifestyle_complete', 'family_complete')


# @admin.register(models.PatientBilling)
# class AdminPatientBilling(admin.ModelAdmin):
#     list_display = ('patient', 'name', 'address1', 'address2', 'city',
#                     'zip', 'card_number', 'cvv_number',
#                     'card_type', 'hsa_card', 'expiration_date')


@admin.register(models.PatientHistory)
class AdminPatientHistory(admin.ModelAdmin):
    list_display = ('patient', 'record_date', 'type', 'provider')


@admin.register(models.PatientHealthHistory)
class AdminPatientHealthHistory(admin.ModelAdmin):
    list_display = ('patient', 'health_conditions', 'medications', 'surgeries')


@admin.register(models.PatientLifestyleQuestion)
class AdminPatientLifestyleQuestion(admin.ModelAdmin):
    list_display = ('question_string',)


@admin.register(models.PatientLifestyle)
class AdminPatientLifestyle(admin.ModelAdmin):
    list_display = ('patient', 'question', 'answer')


@admin.register(models.PatientAppointment)
class AdminPatientAppointment(admin.ModelAdmin):
    list_display = ('case', 'appointment_time',
                    'appointment_type', 'appointment_status')


@admin.register(models.AppointmentNote)
class AdminAppointmentNote(admin.ModelAdmin):
    list_display = ('appointment', 'anamnesis', 'exploration', 'diagnosis',
                    'additional_tests', 'treatment', 'public_notes')


@admin.register(models.PatientFamilyRelationship)
class AdminPatientFamilyRelationship(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.PatientFamilyCondition)
class AdminPatientFamilyCondition(admin.ModelAdmin):
    list_display = ('name', 'patient')


@admin.register(models.PatientFamily)
class AdminPatientFamily(admin.ModelAdmin):
    list_display = ('patient', 'condition', 'relationship')


@admin.register(models.PatientCase)
class AdminPatientCase(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'problem', 'is_second_opinion',
                    'status', 'description')


@admin.register(models.TestFileRecord)
class AdminTestFileRecord(admin.ModelAdmin):
    list_display = (
        'type', 'description', 'request_form', 'result_report_or_record',
        'conclusions', 'requested_by', 'completed_by')


@admin.register(models.AdditionalFile)
class AdminAdditionalFile(admin.ModelAdmin):
    list_display = ('file', 'test_file_record')
