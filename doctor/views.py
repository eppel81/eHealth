import braintree
import datetime as datetime_library
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from allauth.account.views import PasswordChangeView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, \
    HttpResponse, HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.contrib import messages
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from postman.forms import AnonymousWriteForm
from postman.models import Message
from itertools import chain

from ehealth import settings
from doctor import models as doctor_models, forms as doctor_forms
from patient import models as patient_models
from utils import views as utils_views, forms as utils_forms, \
    models as utils_models

from postman import views as postman_views
from utils.views import get_appointment_room_availability


class DoctorMenuViewMixin(utils_views.MenuViewMixin):
    options = [
        {'class': 'fa-bar-chart-o', 'title': _('Dashboard'),
         'href': reverse_lazy('doctor:dashboard')},
        {'class': 'fa-calendar', 'title': _('Calendar'),
         'href': reverse_lazy('doctor:calendar')},
        {'class': 'fa-list-alt', 'title': _('Case'),
         'href': reverse_lazy('doctor:all_cases', kwargs={'type': 'open'})},
        {'class': 'fa-envelope', 'title': _('Message Center'),
         'href': reverse_lazy('doctor:inbox'), 'check_messages': True},
        {'class': 'fa-support', 'title': _('Help & Support'),
         'href': reverse_lazy('doctor:help')},
    ]


class ProfileActiveTabMixin(utils_views.ActiveTabMixin):
    profile_tabs = [
        {'title': _('Specialty'),
         'href': reverse_lazy('doctor:specialty')},
        {'title': _('Work Experience'),
         'href': reverse_lazy('doctor:experience')},
    ]


class CalendarActiveTabMixin(utils_views.ActiveTabMixin):
    tabs = [
        {'title': _('Calendar'),
         'href': reverse_lazy('doctor:calendar')},
        {'title': _('Appointments'),
         'href': reverse_lazy('doctor:appointments')},
    ]


class CaseActiveTabMixin(utils_views.ActiveTabMixin):
    tabs = [
        {'title': _('Open'),
         'href': reverse_lazy('doctor:all_cases', kwargs={'type': 'open'})},
        {'title': _('Close'),
         'href': reverse_lazy('doctor:all_cases', kwargs={'type': 'close'})},
    ]


class AccountActiveTabMixin(utils_views.ActiveTabMixin):
    tabs = [
        {'title': _('Account Details'),
         'img': 'img/my_account.png',
         'href': reverse_lazy('doctor:my_account')},
        {'title': _('Payment information'),
         'img': 'img/payment_info.png',
         'href': reverse_lazy('doctor:payment')},
        {'title': _('Payment History'),
         'img': 'img/payment_history.png',
         'href': reverse_lazy('doctor:payment_history')},
        {'title': _('Change password'),
         'img': 'img/change_password.png',
         'href': reverse_lazy('doctor:password')},
        {'title': _('Account history'),
         'img': 'img/activity.png',
         'href': reverse_lazy('doctor:history')},
        {'title': _('Profile'),
         'img': 'img/profile_info.png',
         'href': reverse_lazy('doctor:specialty')},
    ]


class DashboardView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                    generic.TemplateView):
    active_menu_ind = 0
    template_name = 'doctor/dashboard.html'
    title = _('Dashboard')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        today = timezone.now()
        appointments_status = [
            patient_models.PatientAppointment.STATUS_NEW,
            patient_models.PatientAppointment.STATUS_DOCTOR_APPROVE,
            patient_models.PatientAppointment.STATUS_PATIENT_RESCHEDULE,
        ]
        current_appointments = patient_models.PatientAppointment.objects.filter(
                case__doctor=request.user.doctor,
                appointment_status__in=appointments_status)
        for appointment in current_appointments:
            start_time = appointment.appointment_time.start_time
            duration = appointment.appointment_time.duration
            delta = start_time + datetime_library.timedelta(minutes=duration)
            if start_time <= today <= delta and appointment.appointment_status==patient_models.PatientAppointment.STATUS_DOCTOR_APPROVE:
                today = start_time
        current_appointments = current_appointments.filter(appointment_time__start_time__gte=today)
        context['current_appointments'] = current_appointments
        context['appointment_availability'] = get_appointment_room_availability(current_appointments)

        return self.render_to_response(context)


class MessageCenter(utils_views.DoctorMixin, DoctorMenuViewMixin,
                    generic.TemplateView):
    template_name = 'doctor/dashboard/message_center.html'
    active_menu_ind = 3
    title = _('Message Center')


class HelpSupport(utils_views.DoctorMixin, DoctorMenuViewMixin,
                  generic.TemplateView):
    template_name = 'doctor/dashboard/help_support.html'
    active_menu_ind = 4
    title = _('Help')


class HistoryView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                  AccountActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/account/history.html'
    title = _('My Account')
    active_tab_id = 5

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['history_records'] = doctor_models.DoctorHistory.objects.filter(
            doctor=request.user.doctor)
        return self.render_to_response(context)


class PasswordView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                   utils_views.PasswordChangeTemplateMixin,
                   AccountActiveTabMixin, PasswordChangeView):
    success_url = reverse_lazy("doctor:password")
    form_class = utils_forms.MyChangePassForm
    active_tab_id = 4


class PaymentView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                  AccountActiveTabMixin, generic.FormView):
    template_name = 'doctor/account/payment.html'
    form_class = doctor_forms.PaymentForm
    success_url = reverse_lazy('doctor:payment')
    title = _('Payment')
    active_tab_id = 2
    success_message = _('Payment information updated')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        try:
            payment_info = doctor_models.DoctorPayment.objects.get(
                doctor=self.request.user.doctor)
            return form_class(instance=payment_info, **self.get_form_kwargs())
        except doctor_models.DoctorPayment.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.save()
        return super(PaymentView, self).form_valid(form)


class PaymentHistoryView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                         AccountActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/account/paymenthistory.html'
    title = _('Payment History')
    active_tab_id = 3

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['history_records'] = \
            doctor_models.DoctorPaymentHistory.objects.filter(
                doctor=request.user.doctor)
        return self.render_to_response(context)


class DetailsView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                  AccountActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/account/details.html'
    active_tab_id = 1
    title = _('Account Details')
    success_message = _('Account details updated')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_form'] = utils_forms.DetailUserForm(instance=request.user)
        context['detail_form'] = doctor_forms.DetailForm(
            instance=request.user.doctor)
        return super(DetailsView, self).get(request, *args, **context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_form = utils_forms.DetailUserForm(request.POST,
                                               instance=request.user)
        detail_form = doctor_forms.DetailForm(request.POST, request.FILES,
                                              instance=request.user.doctor)
        if user_form.is_valid() and detail_form.is_valid():
            user_form.save()
            detail_form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(
                redirect_to=reverse_lazy('doctor:my_account'))
        context['user_form'] = user_form
        context['detail_form'] = detail_form
        return render(request, self.template_name, context)


class SpecialtyView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                    AccountActiveTabMixin, ProfileActiveTabMixin,
                    generic.FormView):
    template_name = 'doctor/profile/specialty.html'
    form_class = doctor_forms.SpecialtyForm
    success_url = reverse_lazy('doctor:specialty')
    active_tab_id = 6
    title = _('Specialty')
    success_message = _('Specialties updated')
    profile_active_tab = 1

    def get(self, request, id_specialty=None, *args, **kwargs):
        if id_specialty:
            record = doctor_models.DoctorSpecialty.objects.get(
                pk=id_specialty, doctor=request.user.doctor)
            record.delete()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(
            form=form, specialties=doctor_models.DoctorSpecialty.objects.filter(
                doctor=request.user.doctor)))

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kw = self.get_form_kwargs()
        kw['initial']['exclude_specialty'] = \
            [a.specialty_id for a in
             doctor_models.DoctorSpecialty.objects.filter(
                 doctor=self.request.user.doctor)]
        return form_class(**kw)

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.save()
        return super(SpecialtyView, self).form_valid(form)


class ExperienceView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                     AccountActiveTabMixin, ProfileActiveTabMixin,
                     generic.FormView):
    template_name = 'doctor/profile/workexperience.html'
    form_class = doctor_forms.ExperienceForm
    success_url = reverse_lazy('doctor:experience')
    active_tab_id = 6
    title = _('Work Experience')
    success_message = _('Work experience updated')
    profile_active_tab = 2
    # todo: Empty value!!!

    def get(self, request, id_experience=None, *args, **kwargs):
        if id_experience:
            record = doctor_models.DoctorWorkExperience.objects.get(
                pk=id_experience, doctor=request.user.doctor)
            record.delete()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(
            form=form, works=doctor_models.DoctorWorkExperience.objects.filter(
                doctor=request.user.doctor)))

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.save()
        return super(ExperienceView, self).form_valid(form)


def get_appointment_data(id_appointment, context):
    try:
        patient1 = context.get('patient', '')
        doctor = context.get('doctor', '')
        if patient1:
            appointment = patient_models.PatientAppointment.objects.get(
                pk=id_appointment, case__patient=patient1)
        if doctor:
            appointment = patient_models.PatientAppointment.objects.get(
                pk=id_appointment, case__doctor=doctor)
    except patient_models.PatientAppointment.DoesNotExist:
        return HttpResponse(status=404)
    # todo: Code review!!!
    data = {'type': appointment.get_appointment_type_display()}
    patient = appointment.case.patient
    if patient.user.first_name:
        data['name'] = patient.user.first_name + ' ' + patient.user.last_name
    else:
        data['name'] = patient.user.username
    if patient.health_complete:
        if patient.patienthealthhistory.health_conditions:
            data['health_conditions'] = \
                patient.patienthealthhistory.health_conditions_info
        if patient.patienthealthhistory.medications:
            data['medications'] = patient.patienthealthhistory.medications_info
        if patient.patienthealthhistory.surgeries:
            data['surgeries'] = patient.patienthealthhistory.surgeries_info
    if patient.lifestyle_complete:
        data['weight'] = patient.weight
        data['height_in'] = patient.height_in
        data['height_ft'] = patient.height_ft
        data['questions'] = {}
        questions = patient.patientlifestyle_set.filter(patient=patient)
        for question in questions:
            if question.answer:
                data['questions'].update(
                    {question.question.question_string: 'Yes'})
            else:
                data['questions'].update(
                    {question.question.question_string: 'No'})
    if patient.family_complete:
        data['family'] = {}
        families = patient.patientfamily_set.filter(patient=patient)
        for family in families:
            data['family'].update(
                {family.condition.name: family.relationship.name})
    # files = patient.patientfile_set.filter(patient=patient)
    data['files'] = {}
    # for f in files:
    #     data['files'].update({f.file.name: f.get_type_display})
    data['appointment_id'] = id_appointment
    data['appointment'] = appointment
    return data


class AppointmentsView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                       CalendarActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/schedule/appointments.html'
    active_menu_ind = 1
    active_tab_id = 2
    title = _('Appointments')

    def get(self, request, id_appointment=None, status=None, *args, **kwargs):
        context = self.get_context_data()
        context['doctor'] = self.request.user.doctor
        if status:
            if id_appointment:
                try:
                    appointment = patient_models.PatientAppointment.objects.get(
                        pk=id_appointment)
                except patient_models.PatientAppointment.DoesNotExist:
                    return Http404(**context)
                appointment.appointment_status = int(status)
                s_d_c = patient_models.PatientAppointment.STATUS_DOCTOR_CANCEL
                s_p_c = patient_models.PatientAppointment.STATUS_PATIENT_CANCEL
                if int(status) == s_d_c or int(status) == s_p_c:
                    appointment.appointment_time.free = True
                    appointment.appointment_time.save()
                    transaction_id = appointment.deposit_transaction
                    transaction = braintree.Transaction.find(transaction_id)
                    transaction_status = transaction.status
                    if transaction_status == 'settling' or \
                                    transaction_status == 'settled':
                        result = braintree.Transaction.refund(transaction_id)
                        if result.is_success:
                            appointment.deposit_paid = False
                    elif transaction_status == 'authorized' or \
                        transaction_status == 'submitted_for_settlement':
                        result = braintree.Transaction.void(transaction_id)
                        if result.is_success:
                            appointment.deposit_paid = False
                appointment.save()

                next_link = request.GET.get('next',
                                            reverse_lazy('doctor:appointments'))
                return HttpResponseRedirect(next_link)
            else:
                return Http404(**context)
        # elif id_appointment:
        #     if request.is_ajax():
        #         return render(request, 'doctor/ajax/patient_details.html',
        #                       get_appointment_data(int(id_appointment),
        #                                            context))
        status_choices = [
            patient_models.PatientAppointment.STATUS_NEW,
            patient_models.PatientAppointment.STATUS_DOCTOR_APPROVE,
            patient_models.PatientAppointment.STATUS_DOCTOR_CANCEL,
            patient_models.PatientAppointment.STATUS_PATIENT_CANCEL,
            patient_models.PatientAppointment.STATUS_PATIENT_RESCHEDULE,
            patient_models.PatientAppointment.STATUS_COMPLETE]

        appointments = patient_models.PatientAppointment.objects.filter(
            case__doctor=request.user.doctor,
            appointment_time__start_time__gte=datetime.now().date(),
            appointment_status__in=status_choices, deposit_paid=True) \
            .order_by('appointment_time')
        patient = request.GET.get('patient')
        status = request.GET.get('status')
        if patient:
            appointments = appointments.filter(case__patient__id=patient)
        if status:
            appointments = appointments.filter(appointment_status=status)

        paginator = Paginator(appointments, 10)
        page = request.GET.get('page')
        try:
            context['appointments'] = paginator.page(page)
        except PageNotAnInteger:
            context['appointments'] = paginator.page(1)
        except EmptyPage:
            context['appointments'] = paginator.page(paginator.num_pages)

        patients = patient_models.Patient.objects.filter(
            patientcase__doctor=self.request.user.doctor,
            patientcase__patientappointment__appointment_status__in=
            status_choices,
            patientcase__patientappointment__appointment_time__start_time__gte=
            datetime.now().date(), ).distinct()
        context['patients'] = patients
        all_statuses = {i: str(j) for i, j in
                        patient_models.PatientAppointment.STATUS_CHOICES if
                        i in status_choices}

        context['statuses'] = all_statuses
        context['appointment_availability'] = get_appointment_room_availability(appointments)
        context['current_time'] = timezone.now()

        return super(AppointmentsView, self).get(request, *args, **context)


def gen(start, end, **kwargs):
    cur_date = start
    while cur_date < end:
        cur_date += timedelta(**kwargs)
        yield cur_date


class CalendarView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                   CalendarActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/schedule/calendar.html'
    active_menu_ind = 1
    active_tab_id = 1
    title = _('Calendar')

    def generate_times(self):
        data = []
        for i in xrange(24):
            for j in xrange(0, 60, 15):
                data.append('%02d:%02d' % (i, j))
        return data

    def generate_days(self):
        days = [
            _('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'),
            _('Friday'), _('Saturday'), _('Sunday')
        ]
        return days

    def get_context_data(self, **kwargs):
        data = super(CalendarView, self).get_context_data(**kwargs)
        data['times'] = self.generate_times()
        data['days'] = self.generate_days()
        return data


class TimeView(utils_views.DoctorMixin, generic.FormView):
    success_url = reverse_lazy('doctor:calendar')
    success_message = _('Time updated')
    form_class = doctor_forms.DoctorScheduleFormSet
    template_name = 'doctor/ajax/doctor_schedule.html'

    def _parse_dates(self):
        date_format = "%m/%d/%Y"
        day_from_str = self.request.REQUEST.get('first_day')
        day_to_str = self.request.REQUEST.get('last_day')
        if day_from_str:
            self.day_from = datetime.strptime(day_from_str, date_format)
        else:
            self.day_from = None
        if day_to_str:
            self.day_to = datetime.strptime(day_to_str, date_format)
        else:
            self.day_to = None

    def get_form_queryset(self):
        query = utils_models.AppointmentSchedule.objects.filter(
            doctor=self.request.user.doctor,
            date__range=(self.day_from, self.day_to)
        ).order_by('date')
        return query

    def get_initial(self):
        if not self.day_from or not self.day_to:
            return None
        current_day = self.day_from
        week = [self.day_from, ]
        while current_day != self.day_to:
            current_day = current_day + timedelta(days=1)
            week.append(current_day)
        return [{'date': day.date()} for day in week]

    def get_form_kwargs(self):
        data = super(TimeView, self).get_form_kwargs()
        data['queryset'] = self.get_form_queryset()
        data['request'] = self.request
        return data

    def get(self, request, *args, **kwargs):
        self._parse_dates()
        return super(TimeView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self._parse_dates()
        return super(TimeView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponse()

        # def form_invalid(self, formset):
        #     for form in formset:
        #         if form.is_valid():
        #             form.save()
        #     return super(TimeView, self).form_invalid(form=formset)

        # def post(self, request, *args, **kwargs):
        #     appointment_time = request.POST.getlist('appointment_time')
        #     current_date = request.POST.get('current_date')
        #     next_url = request.GET.get('next')
        #     for time in appointment_time:
        #         arr = time.split('-')
        #         start_time = utils_models.localize_datetime(parse_datetime(current_date + ' ' + arr[0]))
        #         todo:Duration!!!
        # obj, created = doctor_models.DoctorAppointmentTime.objects.get_or_create(
        #     start_time=start_time,
        #     duration=settings.DEFAULT_DURATION,
        #     doctor=request.user.doctor)
        # obj.save()
        # messages.success(request, self.success_message)
        # if next_url:
        #     return HttpResponseRedirect(redirect_to=next_url)
        # return HttpResponseRedirect(redirect_to=self.success_url)


class AppointmentSchedule(utils_views.DoctorMixin, DoctorMenuViewMixin,
                          CalendarActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/schedule/reschedule.html'
    active_menu_ind = 1
    active_tab_id = 2
    title = _('Appointment reschedule')
    success_url = reverse_lazy('doctor:appointments')
    success_message = _('Appointment updated')

    def get(self, request, id_appointment=None, *args, **kwargs):

        next_url = request.GET.get('next')
        if id_appointment:
            try:
                appointment = patient_models.PatientAppointment.objects.get(
                    pk=id_appointment)
            except patient_models.PatientAppointment.DoesNotExist:
                return Http404(**kwargs)
            context = self.get_context_data()
            context['type'] = appointment.get_appointment_type_display()
            context['appointment_id'] = id_appointment
            if appointment.case.patient.user.first_name:
                context['name'] = appointment.case.patient.user.first_name + \
                                  ' ' + appointment.case.patient.user.last_name
            else:
                context['name'] = appointment.case.patient.user.username
            context['appointment_time'] = appointment.appointment_time
            context[
                'times'] = doctor_models.DoctorAppointmentTime.objects.filter(
                start_time__gte=timezone.now().date(), free=True)
            return super(AppointmentSchedule, self).get(request, *args,
                                                        **context)
        if next_url:
            return HttpResponseRedirect(redirect_to=next_url)
        return HttpResponseRedirect(redirect_to=self.success_url)

    def post(self, request, id_appointment=None, *args, **kwargs):
        appointment_time = request.POST.get('appointment_time')
        next_url = request.GET.get('next')
        if appointment_time:
            try:
                appointment = patient_models.PatientAppointment.objects.get(
                    pk=id_appointment)
            except patient_models.PatientAppointment.DoesNotExist:
                return Http404(**kwargs)

            try:
                new_time = doctor_models.DoctorAppointmentTime.objects.get(
                    pk=appointment_time)
                new_time.free = False
                new_time.save()
                appointment.appointment_time.free = True
                appointment.appointment_time.save()
                appointment.appointment_time = new_time
            except doctor_models.DoctorAppointmentTime.DoesNotExist:
                return Http404(**kwargs)
            appointment.appointment_status = \
                patient_models.PatientAppointment.STATUS_DOCTOR_RESCHEDULE
            appointment.save()
            messages.success(request, self.success_message)
            if next_url:
                return HttpResponseRedirect(redirect_to=next_url)
            return HttpResponseRedirect(redirect_to=self.success_url)
        return Http404(**kwargs)


class CaseListView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                   CaseActiveTabMixin, generic.ListView):
    template_name = 'doctor/case/case_list.html'
    active_menu_ind = 2
    active_tab_id = 1
    title = _('Open case')
    type = 'open'
    success_url = reverse_lazy('doctor:all_cases', kwargs={'type': type})
    paginate_by = 10
    context_object_name = 'cases'
    status_choices = [
        patient_models.PatientAppointment.STATUS_NEW,
        patient_models.PatientAppointment.STATUS_DOCTOR_APPROVE,
        patient_models.PatientAppointment.STATUS_DOCTOR_CANCEL,
        patient_models.PatientAppointment.STATUS_PATIENT_CANCEL,
        patient_models.PatientAppointment.STATUS_PATIENT_RESCHEDULE,
        patient_models.PatientAppointment.STATUS_COMPLETE]

    def get_queryset(self):
        queryset = patient_models.PatientCase.objects.filter(
            doctor=self.request.user.doctor,
            patientappointment__isnull=False,
            patientappointment__appointment_status__in=self.status_choices)
        if self.type == 'open':
            queryset = queryset.filter(status=patient_models.PatientCase.OPEN)
        else:
            queryset = queryset.filter(status=patient_models.PatientCase.CLOSED)
        patient = self.request.GET.get('patient')
        search_query = self.request.GET.get('search')
        if patient:
            queryset = queryset.filter(patient__id=patient)
        if search_query:
            queryset = queryset.filter(Q(problem__icontains=search_query) |
                                       Q(description__icontains=search_query))
        queryset = queryset.distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CaseListView, self).get_context_data(**kwargs)
        context['type'] = self.type
        patients = patient_models.Patient.objects.filter(
            patientcase__doctor=self.request.user.doctor,
            patientcase__patientappointment__appointment_status__in=
            self.status_choices).distinct()
        context['patients'] = patients
        return context

    def get(self, request, type=None, *args, **kwargs):
        self.type = type
        if type == 'close':
            self.active_tab_id = 2

        return super(CaseListView, self).get(request, *args, **kwargs)


class CaseMixin(utils_views.DoctorMixin, DoctorMenuViewMixin,
                CaseActiveTabMixin):
    case_tabs = []
    case_tab_id = 0
    active_menu_ind = 2

    def get_active_case_tab(self):
        return self.case_tabs[self.case_tab_id - 1]

    def get_context_data(self, **kwargs):
        context = super(CaseMixin, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        self.case_tabs = [
            {'title': _('Case Overview'),
             'href': reverse_lazy('doctor:case_overview', kwargs={'pk': pk})},
            {'title': _('Appointments & Notes'),
             'href': reverse_lazy('doctor:case_notes', kwargs={'pk': pk})},
            {'title': _('Records and Tests'),
             'href': reverse_lazy('doctor:case_files', kwargs={'pk': pk})},
            {'title': _('Patient History'),
             'href': reverse_lazy('doctor:patient_history', kwargs={'pk': pk})},
            {'title': _('Messages'),
             'href': reverse_lazy('doctor:case_messages', kwargs={'pk': pk})},
        ]
        context['case_tabs'] = self.case_tabs
        if pk:
            try:
                case = patient_models.PatientCase.objects.get(
                    pk=pk, doctor=self.request.user.doctor)
            except ObjectDoesNotExist:
                self.template_name = 'doctor/case/access_denied.html'
                case = None
            context['case'] = case
            if case and case.status:
                self.type = 'open'
                self.active_tab_id = 1
            else:
                self.type = 'close'
                self.active_tab_id = 2
        context['active_tab'] = self.get_active_tab()
        context['active_case_tab'] = self.get_active_case_tab()
        return context


class CaseOverviewView(CaseMixin, generic.DetailView):
    model = patient_models.PatientCase
    template_name = 'doctor/case/overview.html'
    case_tab_id = 1

    def get_object(self, queryset=None):
        try:
            obj = super(CaseOverviewView, self).get_object(queryset)
        except Http404:
            obj = None
        return obj


class CaseNotesView(CaseMixin, generic.ListView):
    model = patient_models.PatientAppointment
    template_name = 'doctor/case/notes.html'
    context_object_name = 'appointments'
    case_tab_id = 2

    def get_context_data(self, **kwargs):
        data = super(CaseNotesView, self).get_context_data(**kwargs)
        data['appointments'] = patient_models.PatientAppointment.objects.filter(
            appointment_time__doctor=self.request.user.doctor,
            case_id=self.kwargs.get('pk'),
            appointment_status__gte=patient_models.PatientAppointment.STATUS_NEW
        )
        return data

    def get_queryset(self):
        case_id = self.kwargs.get('pk')
        return patient_models.PatientAppointment.objects.filter(
            appointment_time__doctor=self.request.user.doctor,
            case_id=case_id,
        )


class CaseFilesView(CaseMixin, generic.ListView):
    model = patient_models.TestFileRecord
    template_name = 'doctor/case/files.html'
    context_object_name = 'files'
    case_tab_id = 3
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CaseFilesView, self).get_context_data(**kwargs)
        context['case_id'] = self.case_id
        model = patient_models.TestFileRecord
        context['types'] = {
            model.TEST: model.STATUS_CHOICES[model.TEST][1],
            model.RECORD: model.STATUS_CHOICES[model.RECORD][1]
            }
        return context

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.case_id = pk
        query = patient_models.TestFileRecord.objects.filter(
                case__doctor=self.request.user.doctor)
        all_files = self.request.GET.get('all_files')
        if all_files:
            patient = patient_models.PatientCase.objects.get(id=pk).patient
            query = query.filter(case__patient=patient)
        else:
            query = query.filter(case__id=self.case_id)

        record_type = self.request.GET.get('type')
        if record_type:
            record_type = int(record_type)
            query = query.filter(type=record_type)
        search_query = self.request.GET.get('search')
        if search_query:
            query = query.filter(description__icontains=search_query)
        return query


class EditFileView(CaseMixin, generic.UpdateView):
    model = patient_models.TestFileRecord
    template_name = 'doctor/case/edit_file.html'
    form_class = doctor_forms.EditFileRecordForm
    pk_url_kwarg = 'id'
    case_tab_id = 2

    def get_success_url(self):
        return reverse_lazy('doctor:all_files',
                            kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True,
                             'url': str(self.get_success_url()),
                             })

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


class CasePatientHistoryView(CaseMixin, generic.DetailView):
    model = patient_models.Patient
    template_name = 'doctor/case/patient_history.html'
    case_tab_id = 4

    def get_object(self, queryset=None):
        case_id = self.kwargs.get('pk')
        obj = patient_models.Patient.objects.get(patientcase=case_id)
        return obj


class CaseMessagesView(CaseMixin, postman_views.FolderMixin,
                       generic.TemplateView):
    template_name = 'postman/case_messages_doctor.html'
    case_tab_id = 5
    folder_name = 'inbox'
    view_name = 'inbox'

    def get_context_data(self, **kwargs):
        context = super(CaseMessagesView, self).get_context_data(**kwargs)
        case_id = self.kwargs.get('pk')
        filters = [Q(casemessage__case_id=case_id) | Q(thread__casemessage__case_id=case_id)]
        inbox = Message.objects.inbox(self.request.user, True).filter(*filters, thread__isnull=True)
        sent = Message.objects.sent(self.request.user).filter(*filters)
        pm_messages = sorted(chain(inbox, sent),
                             key=lambda x: x.sent_at, reverse=True)
        context['pm_messages'] = pm_messages
        return context


# the view is not used
class CaseView(utils_views.DoctorMixin, DoctorMenuViewMixin,
               CaseActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/case/case.html'
    active_menu_ind = 2
    active_tab_id = 1
    title = _('Create case')
    success_url = reverse_lazy('doctor:edit_case')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        # if id_case:
        #     try:
        #         case = patient_models.PatientCase.objects.get(pk=id_case)
        #     except patient_models.PatientCase.DoesNotExist:
        #         case = patient_models.PatientCase(doctor=request.user.doctor)
        #         case.save()
        # else:
        #     case = patient_models.PatientCase(doctor=request.user.doctor)
        #     case.save()

        # context['case'] = case
        context['patients'] = patient_models.Patient.objects.all()
        # context['reasons'] = utils_models.AppointmentReason.objects.all()
        # context['appointments'] = patient_models.PatientAppointment.objects.filter(case__in=[None, case])
        # if id_test:
        #     test = patient_models.Test.objects.get(pk=id_test)
        #     test.delete()
        #     return HttpResponseRedirect(redirect_to=reverse_lazy('doctor:view_case', kwargs={'id_case': case.id},))
        #
        return self.render_to_response(context=context)

    def post(self, request, id_case=None, *args, **kwargs):
        # reason = utils_models.AppointmentReason.objects.get(pk=request.POST.get('reason'))
        patient = patient_models.Patient.objects.get(
            pk=request.POST.get('patient'))
        case = patient_models.PatientCase(doctor=request.user.doctor,
                                          patient=patient)
        case.save()
        # print request['post'].__dict__
        # context = self.get_context_data()
        # if id_case:
        #     try:
        #         case = patient_models.PatientCase.objects.get(pk=id_case)
        #     except patient_models.PatientCase.DoesNotExist:
        #         return Http404(**context)
        # else:
        #     case = patient_models.PatientCase(doctor=request.user.doctor)
        #
        return HttpResponseRedirect(redirect_to=reverse_lazy(
            self.success_url, kwargs={'id_case': case.id}))


# the view is not used
class EditCaseView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                   CaseActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/case/edit_case.html'
    active_menu_ind = 2
    active_tab_id = 1
    title = _('Edit case')
    success_url = reverse_lazy('doctor:edit_case')

    def get(self, request, id_case=None, *args, **kwargs):

        context = self.get_context_data()
        case = patient_models.PatientCase.objects.get(pk=id_case)
        context['patients'] = patient_models.Patient.objects.all()
        context['case'] = case

        if request.is_ajax():
            id_test = request.GET.get('id_test')
            add_test = request.GET.get('add_test')
            if id_test is not None:
                del_test = patient_models.Test.objects.get(pk=id_test)
                del_test.delete()
            # elif add_test is not None:

            tests = patient_models.Test.objects.filter(case=case)
            template = get_template('doctor/ajax/tests.html')
            template_context = Context({'tests': tests, 'case': case})

            return HttpResponse(template.render(template_context))
        return self.render_to_response(context=context)


class DoctorAppointmentsJSON(utils_views.DoctorMixin, generic.View):
    def get(self, *args, **kwargs):
        date_format = "%m/%d/%Y"
        tz = timezone.get_current_timezone()
        fday_week = tz.localize(
            datetime.strptime(self.request.GET.get('first_day'), date_format))
        lday_week = tz.localize(
            datetime.strptime(self.request.GET.get('last_day'), date_format))
        doctor = self.request.user.doctor
        data = []
        query = doctor_models.DoctorAppointmentTime.objects.filter(
            doctor=doctor)
        query = query.filter(
            start_time__range=(fday_week, lday_week + timedelta(days=1)))

        for date in query:
            tmp = {}
            tmp.update({
                'id': date.id,
                'day': date.start_time.astimezone(tz).strftime("%A"),
                'time': date.start_time.astimezone(tz).strftime("%H:%M"),
                'free': date.free,
                'duration': date.duration
            })
            appointment = date.patientappointment_set.exclude(Q(
                appointment_status=patient_models.PatientAppointment.STATUS_EDIT) |
                                                              Q(
                                                                  appointment_status=patient_models.PatientAppointment.STATUS_DOCTOR_CANCEL) |
                                                              Q(
                                                                  appointment_status=patient_models.PatientAppointment.STATUS_PATIENT_CANCEL)).first()
            if appointment:
                tmp.update({
                    'patient': str(appointment.case.patient),
                    'case_url': str(reverse_lazy('doctor:case_overview',
                                                 kwargs={
                                                     'pk': appointment.case.id}))
                })
            data.append(tmp)

        return JsonResponse(data, safe=False)


class EditNoteView(utils_views.DoctorMixin, generic.UpdateView):
    form_class = doctor_forms.NoteForm
    model = patient_models.AppointmentNote
    template_name = 'doctor/case/edit_note.html'
    context_object_name = 'note'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return HttpResponse()

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


class AllPatientNotesView(utils_views.DoctorMixin, generic.TemplateView):
    model = patient_models.PatientAppointment
    template_name = 'doctor/case/all_notes.html'
    context_object_name = 'appointments'

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()
        patient_id = self.kwargs.get('patient')
        column = request.GET.get('key', '')
        case_id = self.kwargs.get('case')
        order = request.GET.get('order', '')
        if order:
            column += '_desc'
        patient = patient_models.Patient.objects.get(id=patient_id)
        query = patient_models.PatientAppointment.objects.filter(
            case_id=case_id).filter(case__patient=patient,
                                    case__doctor=self.request.user.doctor)

        dict_query = {
            'diagnosis': 'appointmentnote__diagnosis',
            'diagnosis_desc': '-appointmentnote__diagnosis',
            'anamnesis': 'appointmentnote__anamnesis',
            'anamnesis_desc': '-appointmentnote__anamnesis',
            'exploration': 'appointmentnote__exploration',
            'exploration_desc': '-appointmentnote__exploration',
            'additional_tests': 'appointmentnote__additional_tests',
            'additional_tests_desc': '-appointmentnote__additional_tests',
            'date': 'appointment_time__start_time',
            'date_desc': '-appointment_time__start_time',
            'treatment': 'appointmentnote__treatment',
            'treatment_desc': '-appointmentnote__treatment',
            'public_notes': 'appointmentnote__public_notes',
            'public_notes_desc': '-appointmentnote__public_notes',
        }

        if column:
            context['appointments'] = query.order_by(dict_query.get(column))
        else:
            context['appointments'] = query
        return render(request, 'doctor/case/all_notes.html', context)


class NoteDetailsView(utils_views.DoctorMixin, generic.TemplateView):
    template_name = 'doctor/ajax/file_details.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        file_id = request.GET.get('file')
        test_file_record = patient_models.TestFileRecord.objects.get(id=file_id)
        context.update({'file': test_file_record})
        return self.render_to_response(context=context)


class DoctorMessageActiveTabMixin(utils_views.ActiveTabMixin):
    message_tabs = [
        {'class': 'message_in',
         'href': reverse_lazy('doctor:inbox'),
         'title': _('Inbox'),
         },
        {'class': 'message_out',
         'href': reverse_lazy('doctor:sent'),
         'title': _('Sent'),
         },
        {'class': 'message_lock',
         'href': reverse_lazy('doctor:archives'),
         'title': _('Archived'),
         },
        {'class': 'message_ban',
         'href': reverse_lazy('doctor:trash'),
         'title': _('Deleted'),
         },
        {'class': 'pen',
         'href': reverse_lazy('doctor:write_message_patient'),
         'title': _('Send message to'),
         },
    ]


class MessageFolderMixin(object):
    title = _('Message Center')

    def get_context_data(self, **kwargs):
        option = kwargs.get('option')
        context = super(MessageFolderMixin, self).get_context_data(
            option=option)
        user_type = 'patient' if self.request.user else 'doctor'
        viewname = user_type + ':' + self.view_name
        current_instance = self.request.resolver_match.namespace
        context['by_message_url'] = reverse(viewname, args=[
            postman_views.OPTION_MESSAGES], current_app=current_instance)
        context['by_conversation_url'] = reverse(viewname,
                                                 current_app=current_instance)
        return context


class InboxMessagesView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                        DoctorMessageActiveTabMixin, MessageFolderMixin,
                        postman_views.InboxView):
    active_menu_ind = 3
    message_active_tab = 1


class SentMessagesView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                       DoctorMessageActiveTabMixin, MessageFolderMixin,
                       postman_views.SentView):
    active_menu_ind = 3
    message_active_tab = 2


class ArchivedMessagesView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                           DoctorMessageActiveTabMixin, MessageFolderMixin,
                           postman_views.ArchivesView):
    active_menu_ind = 3
    message_active_tab = 3


class DeletedMessagesView(utils_views.DoctorMixin, DoctorMenuViewMixin,
                          DoctorMessageActiveTabMixin, MessageFolderMixin,
                          postman_views.TrashView):
    active_menu_ind = 3
    message_active_tab = 4


class ShowMessageView(utils_views.DoctorMixin, postman_views.MessageView):
    template_name = 'postman/message_view.html'


class ShowConversationView(utils_views.DoctorMixin,
                           postman_views.ConversationView):
    template_name = 'postman/message_view.html'


class WriteMessageMixin(utils_views.DoctorMixin,
                        DoctorMenuViewMixin, DoctorMessageActiveTabMixin):
    write_message_tabs = []
    write_message_active_tab = 0
    active_menu_ind = 3
    message_active_tab = 5

    def get_active_write_message_tab(self):
        return self.write_message_tabs[self.write_message_active_tab - 1]

    def get_context_data(self, **kwargs):
        context = super(WriteMessageMixin, self).get_context_data(**kwargs)
        self.write_message_tabs = [
            {'title': _('Patient'),
             'href': reverse_lazy('doctor:write_message_patient'),
            },
            {'title': _('Doctor'),
             'href': reverse_lazy('doctor:write_message_doctor'),
            },
            {'title': _('Support'),
             'href': reverse_lazy('doctor:write_message_support'),
            },
        ]
        context['write_message_tabs'] = self.write_message_tabs
        context['write_message_active_tab'] = self.get_active_write_message_tab()
        return context


class WritePatientMessageView(WriteMessageMixin, postman_views.WriteView):
    template_name = 'postman/write_to_doctor.html'
    write_message_active_tab = 1
    form_classes = (doctor_forms.WriteMessageForm, AnonymousWriteForm)
    success_url = reverse_lazy('doctor:sent')

    def get_form(self, form_class=None):
        form = super(WritePatientMessageView, self).get_form(form_class)
        doctor = self.request.user.doctor
        # form.fields['case'].queryset = patient_models.PatientCase.objects.filter(
        #     doctor=doctor)
        form.fields['recipients'].queryset = User.objects.filter(
            patient__isnull=False,
            patient__patientcase__doctor=doctor).distinct()
        return form


class SendNewMessageView(WritePatientMessageView):
    template_name = 'postman/write_to_case_doctor.html'

    def get_form(self, form_class=None):
        form = super(SendNewMessageView, self).get_form(form_class)
        case_id = self.kwargs.get('pk')
        case_queryset = patient_models.PatientCase.objects.filter(id=case_id)
        case = case_queryset.get()
        patient_user = case.patient.user
        form.fields['case'].queryset = case_queryset
        form.fields['recipients'].queryset = User.objects.filter(
            pk=patient_user.pk)
        form.fields['recipients'].initial = patient_user
        form.fields['case'].initial = case
        return form

    def form_valid(self, form):
        message = form.save()
        return JsonResponse({
            'redirect': True,
            'success': True,
            'url': str(reverse_lazy('doctor:case_messages',
                                    kwargs={'pk': message.casemessage.case.pk}))
        })

    def form_invalid(self, form):
        data = {
            'success': False,
            'errors': form.errors
        }
        return JsonResponse(data)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = super(SendNewMessageView, self).get_success_url()
        return next_url


class WriteDoctorMessageView(WriteMessageMixin, postman_views.WriteView):
    template_name = 'postman/write_to_doctor.html'
    write_message_active_tab = 2
    form_classes = (doctor_forms.WriteDoctorMessageForm, AnonymousWriteForm)
    success_url = reverse_lazy('doctor:sent')

    def get_form(self, form_class=None):
        form = super(WriteDoctorMessageView, self).get_form(form_class)
        doctor = self.request.user.doctor
        form.fields['recipients'].queryset = User.objects.filter(
            doctor__isnull=False).exclude(doctor=doctor).distinct()
        return form


class WriteSupportMessageView(WriteMessageMixin, postman_views.WriteView):
    template_name = 'postman/write_to_doctor.html'
    write_message_active_tab = 3
    form_classes = (doctor_forms.WriteMessageSupportForm, AnonymousWriteForm)
    success_url = reverse_lazy('doctor:sent')


def get_all_cases_json(request):
    pk = request.GET.get('pk')
    doctor = request.user.doctor
    data = {}
    query = patient_models.PatientCase.objects.filter(patient__user__id=pk,
                                                      doctor=doctor)
    if query:
        for item in query:
            data.update({item.pk: item.problem[:40]})
    # data.update({'': str(_('Select'))})
    return JsonResponse(data)

