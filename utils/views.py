import braintree
import datetime
import opentok
from django.utils import timezone
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.encoding import force_text
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.views import generic
from django.utils.translation import ugettext_lazy as _


import patient.models as patient_models
import doctor.models as doctor_models


class MenuViewMixin(SuccessMessageMixin):
    options = []
    title = ''
    active_menu_ind = 0
    app_process = ''

    def get_active_menu(self):
        return self.options[self.active_menu_ind]

    def get_context_data(self, **kwargs):
        data = super(MenuViewMixin, self).get_context_data(**kwargs)
        data['menus'] = self.options
        data['active_menu'] = self.get_active_menu()
        data['title'] = self.title
        data['app_process'] = self.app_process
        return data


class ActiveTabMixin(object):
    base_tabs = []
    tabs = []
    profile_tabs = []
    process = []
    process1 = []
    message_tabs = []
    active_tab_id = 0
    active_proc = 0
    active_proc1 = 0
    base_active_tab = 0
    profile_active_tab = 0
    message_active_tab = 0

    def get_base_active_tab(self):
        return self.base_tabs[self.base_active_tab - 1]

    def get_profile_active_tab(self):
        return self.profile_tabs[self.profile_active_tab - 1]

    def get_active_tab(self):
        return self.tabs[self.active_tab_id - 1]

    def get_active_proc(self):
        # for item in self.process:
        #     if item['number'] <= self.active_proc:
        #         item['finished'] = True
        return self.process[self.active_proc - 1]

    def get_active_proc1(self):
        return self.process1[self.active_proc1 - 1]

    def get_message_active_tab(self):
        return self.message_tabs[self.message_active_tab - 1]

    def get_context_data(self, **kwargs):
        data = super(ActiveTabMixin, self).get_context_data(**kwargs)
        data['base_tabs'] = self.base_tabs
        if self.base_active_tab > 0:
            data['base_active_tab'] = self.get_base_active_tab()

        data['message_tabs'] = self.message_tabs
        if self.message_active_tab > 0:
            data['message_active_tab'] = self.get_message_active_tab()

        data['profile_tabs'] = self.profile_tabs
        if self.profile_active_tab > 0:
            data['profile_active_tab'] = self.get_profile_active_tab()
        data['tabs'] = self.tabs
        if self.active_tab_id > 0:
            data['active_tab'] = self.get_active_tab()
        data['process'] = self.process
        if self.process:
            data['active_proc'] = self.get_active_proc()

        data['process1'] = self.process1
        if self.process1:
            data['active_proc1'] = self.get_active_proc1()

        return data


def home(request):
    if request.user.is_authenticated():
        if request.session['type_user'] == 'patient':
            return HttpResponseRedirect(
                redirect_to=reverse('patient:dashboard'))
        elif request.session['type_user'] == 'doctor':
            return HttpResponseRedirect(redirect_to=reverse('doctor:dashboard'))
    else:
        list(messages.get_messages(request))
    return render(request, 'home.html')


def terms(request):
    return render(request, 'terms.html')


def about(request):
    return render(request, 'about.html')


class AccessMixin(object):
    login_url = None
    permission_denied_message = "You don't have right to access this page"
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return force_text(login_url)

    def get_permission_denied_message(self):
        return self.permission_denied_message

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class LoginRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.handle_no_permission()
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class UserPassesTestMixin(AccessMixin):
    def test_func(self):
        raise NotImplementedError(
            '{0} is missing the implementation of the test_func() method.'.format(self.__class__.__name__)
        )

    def get_test_func(self):
        return self.test_func

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return self.handle_no_permission()
        return super(UserPassesTestMixin, self).dispatch(request, *args, **kwargs)


class PatientMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return hasattr(self.request.user, 'patient')

    def handle_no_permission(self):
        if self.request.user.is_authenticated() and self.raise_exception:
            # raise PermissionDenied(self.get_permission_denied_message())
            return HttpResponseRedirect(reverse_lazy('doctor:dashboard'))
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class DoctorMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return hasattr(self.request.user, 'doctor')

    def handle_no_permission(self):
        if self.request.user.is_authenticated() and self.raise_exception:
            # raise PermissionDenied(self.get_permission_denied_message())
            return HttpResponseRedirect(reverse_lazy('patient:dashboard'))
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())


class PasswordChangeTemplateMixin(object):
    def get_context_data(self, **kwargs):
        data = super(PasswordChangeTemplateMixin, self).get_context_data(
            **kwargs)
        data['user_type_template'] = \
            self.request.session['type_user'] + '/account/base_account.html'
        data['form_action_url'] = \
            self.request.session['type_user'] + ':password'
        return data



class DoctorAppointmentRoom(DoctorMixin, generic.TemplateView):
    template_name = 'appointment_room/doctor.html'


class PatientAppointmentRoom(PatientMixin, generic.TemplateView):
    template_name = 'appointment_room/patient.html'


class AppointmentRoom(LoginRequiredMixin, generic.TemplateView):
    template_name = 'appointment_room/diagnostics.html'
    failure_message = _('Something went wrong. Please check your payment info')

    def get(self, request, *args, **kwargs):
        case_id = self.kwargs.get('pk')
        case = patient_models.PatientCase.objects.get(id=case_id)
        doctor = doctor_models.Doctor.objects.get(patientcase=case)
        appointment_id = self.kwargs.get('appointment')
        appointment = patient_models.PatientAppointment.objects.get(id=appointment_id)

        if request.is_ajax():
            session_id = case.opentok_session
            api_key = settings.OPENTOK_API_KEY
            api_secret = settings.OPENTOK_API_SECRET
            opentok_instance = opentok.OpenTok(api_key, api_secret)
            token = opentok_instance.generate_token(session_id)
            if not appointment.opentok_token:
                appointment.opentok_token = token
                appointment.save()
            doctor_name = str(doctor)
            doctor_specialty = ' '.join([i.specialty.name for i in
                                         doctor.doctorspecialty_set.all()])
            doctor_gender = str(dict(doctor_models.Doctor.GENDER_CHOICES)
                                [doctor.gender])
            if doctor.city and doctor.country:
                doctor_location = doctor.city.name + ', ' + doctor.country.name
            elif doctor.city:
                doctor_location = doctor.city.name
            elif doctor.country:
                doctor_location = doctor.country.name
            else:
                doctor_location = None

            doctor_short_info = doctor_specialty
            if doctor_location:
                doctor_short_info += " (" + doctor_location + ")"

            doctor_info = {
                'Name': doctor_name,
                'Info': doctor_short_info,
                'Specialty': doctor_specialty,
                'Gender': doctor_gender,
                'Location': doctor_location
            }

            patient = patient_models.Patient.objects.get(patientcase=case)
            patient_name = str(patient)
            patient_height = str(patient.height_ft) + ' ft '
            if patient.height_in:
                patient_height += str(patient.height_in) + ' in'
            patient_weight = str(patient_height) + ' lbs'
            patient_location = patient.country.name if patient.country else\
                "Not specified"

            patient_info = {
                'Name': patient_name,
                'Height': patient_height,
                'Weight': patient_weight,
                'Location': patient_location
            }
            notes = str(appointment.appointmentnote.public_notes)

            return JsonResponse({
                'api_key': api_key,
                'session_id': session_id,
                'token': token,
                'doctor_info': doctor_info,
                'patient_info': patient_info,
                'notes': notes

            })
        person = getattr(request.user, 'patient', None)
        if person:
            nonce_from_the_client = self.request.GET.get('payment_method_nonce')
            customer_id = self.request.user.customeruser.customer
            result = braintree.Transaction.sale({
                "customer_id": str(customer_id),
                "amount": str(doctor.consult_rate-doctor.deposit),
                "merchant_account_id": settings.MERCHANT_ID,
                "payment_method_nonce": nonce_from_the_client,
                "custom_fields": {
                    "type": "Consult Rate",
                    "appointment_date": appointment.appointment_time.start_time,
                    "case": case.problem
                },

                "options": {
                    "submit_for_settlement": False,
                }
            })
            if result.is_success:
                appointment.consult_paid = True
                appointment.consult_transaction = result.transaction.id
                appointment.save()
                return super(AppointmentRoom, self).get(request, *args, **kwargs)
            else:
                messages.error(request, self.failure_message)
                redirect_url = reverse_lazy('patient:payment')
                redirect_url += '?next_url=' + str(
                    reverse_lazy('utils:appointment_room',
                                 kwargs={'pk': case_id,
                                         'appointment': appointment_id}))

            return HttpResponseRedirect(redirect_url)
        else:
            return super(AppointmentRoom, self).get(request, *args, **kwargs)


def billing_checkout(request):
    consult_rate = 10
    if request.is_ajax():
        customer = request.user.customeruser.customer
        client_token = braintree.ClientToken.generate({
            "customer_id": customer
                })
        return JsonResponse({
            'client_token': client_token,
            'consult_rate': consult_rate})
    nonce_from_the_client = request.POST.get('payment_method_nonce')
    if nonce_from_the_client:
        result = braintree.Transaction.sale({
            "amount": str(consult_rate),
            "payment_method_nonce": nonce_from_the_client,
            "options": {
              "submit_for_settlement": True
            }
        })
    return HttpResponseRedirect(redirect_to=reverse_lazy('patient:billing'))


def get_appointment_room_availability(all_appointments):
    current_time = timezone.now()
    appointment_availability = dict()
    appointment_editability = dict()
    if settings.DEBUG:
        for appointment in all_appointments:
            appointment_time = appointment.appointment_time.start_time
            appointment_duration = appointment.appointment_time.duration

            appointment_show_from = appointment_time - datetime.timedelta(
                minutes=30)
            appointment_show_to = appointment_time + datetime.timedelta(
                minutes=appointment_duration)

            appointment_available_from = appointment_time - datetime.timedelta(
                minutes=5)
            appointment_available_to = appointment_show_to

            if appointment_show_to >= current_time >= appointment_show_from:
                appointment_availability[appointment.id] = [True]
                remain_time = appointment_available_from - current_time
                remain_time = int((remain_time.total_seconds() % 3600) // 60) + 1
                appointment_availability[appointment.id].append(
                    remain_time if current_time <= appointment_available_from
                    else 0)
            else:
                appointment_availability[appointment.id] = [False]

            appointment_availability[appointment.id].append(
                True if appointment_available_to >= current_time >=
                        appointment_available_from else False)

            appointment_editability_to = appointment_time - datetime.timedelta(
                days=1)
            appointment_editability[appointment.id] = (
                True if appointment_editability_to >= current_time else False)
    else:
        appointment_availability = {appointment.id: [True, 0, True]
                                    for appointment in all_appointments}
        appointment_editability = {appointment.id: True
                                   for appointment in all_appointments}
    return appointment_availability, appointment_editability
