from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^terms/$', views.home, name='terms_conditions'),
    url(r'^about/$', views.about, name='about_us'),
    url(r'^appointment_room/(?P<pk>\d+)/(?P<appointment>\d+)/$', views.AppointmentRoom.as_view(), name='appointment_room'),

    # url(r'^appointment_room/$', views.AppointmentRoom.as_view(), name='appointment_room'),
    url(r'^appointment_room/doctor/$', views.DoctorAppointmentRoom.as_view(), name='appointment_room_doctor'),
    url(r'^appointment_room/patient/$', views.PatientAppointmentRoom.as_view(), name='appointment_room_patient'),
    url(r'^google7927943e73d9551e.html$', views.generic.TemplateView.as_view(template_name='appointment_room/google7927943e73d9551e.html'), name='appointment_room_confirmation'),
    url(r'^billing/checkout$', views.billing_checkout, name='checkout'),



]
