from django.conf.urls import url
from postman import OPTIONS
from postman import views as postman_views

from patient import views
from patient import forms

urlpatterns = [
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/talk-to-a-doctor/$', views.TalkToADoctor.as_view(), name='talk_to_a_doctor'),
    url(r'^dashboard/history/$', views.MyHealthHistory.as_view(), name='my_health_history'),
    url(r'^dashboard/lifestyle/$', views.MyLifestyle.as_view(), name='my_lifestyle'),
    url(r'^dashboard/family/$', views.MyFamilyHistory.as_view(), name='my_family_history'),
    url(r'^dashboard/support/$', views.HelpSupport.as_view(), name='help'),
    # url(r'^dashboard/messagecenter/$', views.MessageCenter.as_view(), name='messages'),
    url(r'^dashboard/records/$', views.MyRecords.as_view(), name='my_records'),
    # url(r'^dashboard/records/(?P<id_file>.+)/$', views.MyRecords.as_view(), name='my_records_delete'),
    url(r'^dashboard/support/$', views.HelpSupport.as_view(), name='help'),
    url(r'^dashboard/consultations/$', views.ConsultationView.as_view(), name='consultation'),
    url(r'^dashboard/consultations/status/(?P<id_appointment>\d+)/(?P<status>\d+)/$',
        views.ConsultationView.as_view(), name='consultation_status'),
    url(r'^dashboard/consultations/edit/(?P<pk>\d+)/$',
        views.ConsultationEdit.as_view(), name='consultation_edit'),

    url(r'^my_account/history/$', views.HistoryView.as_view(), name='history'),
    url(r'^my_account/password/$', views.PasswordView.as_view(), name='password'),
    url(r'^my_account/billing/$', views.BillingView.as_view(), name='billing'),
    url(r'^my_account/details/$', views.DetailsView.as_view(), name='my_account'),
    url(r'^my_account/payment/$', views.PaymentView.as_view(), name='payment'),

    url(r'^appointment_request/(?P<pk>[0-9]+)/$', views.PatientAppointmentView.as_view(), name='appointment_request'),
    url(r'^appointment_process/$', views.PatientAppointmentProcessView.as_view(), name='appointment_process'),
    url(r'^appointment_process1/$', views.PatientAppointmentProcess1View.as_view(), name='appointment_process1'),
    url(r'^appointment_process/confirmation/$', views.ConfirmAppointmentProcessView.as_view(), name='confirmation'),
    url(r'^doctor/(?P<pk>[0-9]+)/$', views.DoctorDetailView.as_view(), name='detail_doctor'),
    url(r'^all_doctors/$', views.get_all_doctors_json, name='all_doctors'),
    url(r'^doctor_appointment_time/$', views.get_doctor_appointment_time, name='doctor_time'),
    url(r'^cases/(?P<type>\w+)/$', views.PatientCaseListView.as_view(), name='all_cases'),
    url(r'^case_appointment/(?P<pk>\d+)/$', views.PatientCaseAppointmentView.as_view(), name='case_appointment'),
    url(r'^case_appointment/payment/(?P<pk>\d+)/(?P<appointment>\d+)/$', views.AppointmentDepositPayment.as_view(), name='appointment_payment'),
    url(r'^case_appointment/rate_payment/(?P<pk>\d+)/(?P<appointment>\d+)/$', views.AppointmentRatePayment.as_view(), name='after_appointment'),
    url(r'^case_files/(?P<pk>\d+)/$', views.PatientCaseFilesView.as_view(), name='case_files'),
    url(r'^case_overview/(?P<pk>\d+)/$', views.PatientCaseDetailView.as_view(), name='case_overview'),
    url(r'^add_file/(?P<pk>\d+)/$', views.PatientCaseAddFileView.as_view(), name='add_file'),
    url(r'^delete_file/(?P<pk>\d+)/(?P<case>\d+)/$', views.PatientTestFileRecordDeleteView.as_view(), name='delete_file'),
    url(r'^case_notes/(?P<pk>\d+)/$', views.PatientCaseNoteView.as_view(), name='doctor_notes'),
    url(r'^case_messages/(?P<pk>\d+)/', views.PatientCaseMessagesView.as_view(), name='case_messages'),


    url(r'^history/$', views.PatientHealthHistoryProcess.as_view(), name='health_history_proc'),
    url(r'^lifestyle/$', views.PatientLifestyleProcess.as_view(), name='lifestyle_proc'),
    url(r'^family/$', views.PatientFamilyHistoryProcess.as_view(), name='family_history_proc'),
    # url(r'^payment/$', views.PatientPaymentProcess.as_view(), name='payment_proc'),
    url(r'^confirm/$', views.ConfirmProcessView.as_view(), name='confirm'),

    url(r'^inbox/(?:(?P<option>'+OPTIONS+')/)?$', views.InboxMessagesView.as_view(), name='inbox'),
    url(r'^sent/(?:(?P<option>'+OPTIONS+')/)?$', views.SentMessagesView.as_view(), name='sent'),
    url(r'^archives/(?:(?P<option>'+OPTIONS+')/)?$', views.ArchivedMessagesView.as_view(), name='archives'),
    url(r'^trash/(?:(?P<option>'+OPTIONS+')/)?$', views.DeletedMessagesView.as_view(), name='trash'),
    url(r'^view/(?P<message_id>[\d]+)/$', views.ShowMessageView.as_view(), name='message_view'),
    url(r'^view/t/(?P<thread_id>[\d]+)/$', views.ShowConversationView.as_view(), name='view_conversation'),
    url(r'^write_doctor/(?:(?P<recipients>[^/#]+)/)?$', views.WriteDoctorMessageView.as_view(), name='write_message_doctor'),
    url(r'^write_support/(?:(?P<recipients>[^/#]+)/)?$', views.WriteSupportMessageView.as_view(), name='write_message_support'),

    # url(r'^reply/(?P<message_id>[\d]+)/$', views.ReplyMessageView.as_view(), name='reply_message'),

    url(r'^get_doctor_cases/$', views.get_all_cases_json, name='get_cases'),
    url(r'^get_doctor_day_schedule/$', views.get_doctor_day_schedule, name='get_doctor_day_schedule'),
    url(r'^send_new/(?P<pk>\d+)/$', views.SendNewMessage.as_view(), name='send_new'),



    # url(r'^write/(?:(?P<recipients>[^/#]+)/)?$', views.WriteMessageView.as_view(), name='write'),
    # url(r'^reply/(?P<message_id>[\d]+)/$', ReplyView.as_view(), name='reply'),
    # url(r'^view/(?P<message_id>[\d]+)/$', MessageView.as_view(), name='view'),
    # url(r'^view/t/(?P<thread_id>[\d]+)/$', ConversationView.as_view(), name='view_conversation'),
    # url(r'^archive/$', ArchiveView.as_view(), name='archive'),
    # url(r'^delete/$', DeleteView.as_view(), name='delete'),
    # url(r'^undelete/$', UndeleteView.as_view(), name='undelete'),
    # (r'^$', RedirectView.as_view(url='inbox/', permanent=True)),

]