from django.utils import timezone
from datetime import datetime, timedelta
from allauth.account.views import PasswordChangeView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from doctor import models as doctor_models, forms as doctor_forms
from patient import models as patient_models
from utils import views as utils_views, forms as utils_forms, models as utils_models
from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template


class DoctorMenuViewMixin(utils_views.MenuViewMixin):
    options = [
        {'class': 'fa-bar-chart-o', 'title': _('Dashboard'),
         'href': reverse_lazy('doctor:dashboard')},
        {'class': 'fa-calendar', 'title': _('Calendar'),
         'href': reverse_lazy('doctor:calendar')},
        {'class': 'fa-list-alt', 'title': _('Case'),
         'href': reverse_lazy('doctor:case', kwargs={'type': 'open'})},
        {'class': 'fa-envelope', 'title': _('Message Center'),
         'href': reverse_lazy('doctor:messages')},
        {'class': 'fa-support', 'title': _('Help & Support'),
         'href': reverse_lazy('doctor:help')},
    ]


class ProfileActiveTabMixin(utils_views.ActiveTabMixin):
    tabs = [
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
         'href': reverse_lazy('doctor:case', kwargs={'type': 'open'})},
        {'title': _('Close'),
         'href': reverse_lazy('doctor:case', kwargs={'type': 'close'})},
    ]


class AccountActiveTabMixin(utils_views.ActiveTabMixin):
    tabs = [
        {'title': _('Account Details'),
         'href': reverse_lazy('doctor:my_account')},
        {'title': _('Payment information'),
         'href': reverse_lazy('doctor:payment')},
        {'title': _('Payment History'),
         'href': reverse_lazy('doctor:payment_history')},
        {'title': _('Change password'),
         'href': reverse_lazy('doctor:password')},
        {'title': _('Account history'),
         'href': reverse_lazy('doctor:history')},
    ]


class DashboardView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, generic.TemplateView):
    active_menu_ind = 0
    template_name = 'doctor/dashboard.html'
    title = _('Dashboard')


class MessageCenter(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, generic.TemplateView):
    template_name = 'doctor/dashboard/message_center.html'
    active_menu_ind = 3
    title = _('Message Center')


class HelpSupport(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, generic.TemplateView):
    template_name = 'doctor/dashboard/help_support.html'
    active_menu_ind = 4
    title = _('Help')


class HistoryView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, AccountActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/account/history.html'
    title = _('My Account')
    active_tab_id = 5

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['history_records'] = doctor_models.DoctorHistory.objects.filter(doctor=request.user.doctor)
        return self.render_to_response(context)


class PasswordView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, utils_views.PasswordChangeTemplateMixin,
                   AccountActiveTabMixin, PasswordChangeView):
    success_url = reverse_lazy("doctor:password")
    form_class = utils_forms.MyChangePassForm
    active_tab_id = 4


class PaymentView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, AccountActiveTabMixin, generic.FormView):
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
            payment_info = doctor_models.DoctorPayment.objects.get(doctor=self.request.user.doctor)
            return form_class(instance=payment_info, **self.get_form_kwargs())
        except doctor_models.DoctorPayment.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.save()
        return super(PaymentView, self).form_valid(form)


class PaymentHistoryView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin,
                         AccountActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/account/paymenthistory.html'
    title = _('Payment History')
    active_tab_id = 3

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['history_records'] = doctor_models.DoctorPaymentHistory.objects.filter(doctor=request.user.doctor)
        return self.render_to_response(context)


class DetailsView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, AccountActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/account/details.html'
    active_tab_id = 1
    title = _('Account Details')
    success_message = _('Account details updated')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_form'] = utils_forms.DetailUserForm(instance=request.user)
        context['detail_form'] = doctor_forms.DetailForm(instance=request.user.doctor)
        return super(DetailsView, self).get(request, *args, **context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print request.FILES
        user_form = utils_forms.DetailUserForm(request.POST, instance=request.user)
        detail_form = doctor_forms.DetailForm(request.POST, request.FILES, instance=request.user.doctor)
        if user_form.is_valid() and detail_form.is_valid():
            user_form.save()
            detail_form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(redirect_to=reverse_lazy('doctor:my_account'))
        context['user_form'] = user_form
        context['detail_form'] = detail_form
        return render(request, self.template_name, context)


class SpecialtyView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, ProfileActiveTabMixin, generic.FormView):
    template_name = 'doctor/profile/specialty.html'
    form_class = doctor_forms.SpecialtyForm
    success_url = reverse_lazy('doctor:specialty')
    active_tab_id = 1
    title = _('Specialty')
    success_message = _('Specialties updated')

    def get(self, request, id_specialty=None, *args, **kwargs):
        if id_specialty:
            record = doctor_models.DoctorSpecialty.objects.get(pk=id_specialty, doctor=request.user.doctor)
            record.delete()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form,
                                                             specialties=doctor_models.DoctorSpecialty.objects.filter(
                                                                 doctor=request.user.doctor)))

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kw = self.get_form_kwargs()
        kw['initial']['exclude_specialty'] = [a.specialty_id for a in doctor_models.DoctorSpecialty.objects.filter(
            doctor=self.request.user.doctor)]
        return form_class(**kw)

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.save()
        return super(SpecialtyView, self).form_valid(form)


class ExperienceView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, ProfileActiveTabMixin, generic.FormView):
    template_name = 'doctor/profile/workexperience.html'
    form_class = doctor_forms.ExperienceForm
    success_url = reverse_lazy('doctor:experience')
    active_tab_id = 2
    title = _('Work Experience')
    success_message = _('Work experience updated')
    # todo: Empty value!!!

    def get(self, request, id_experience=None, *args, **kwargs):
        if id_experience:
            record = doctor_models.DoctorWorkExperience.objects.get(pk=id_experience, doctor=request.user.doctor)
            record.delete()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form,
                                                             works=doctor_models.DoctorWorkExperience.objects.filter(
                                                                 doctor=request.user.doctor)))

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor
        form.save()
        return super(ExperienceView, self).form_valid(form)


def get_appointment_data(id_appointment, context):
    try:
        appointment = patient_models.PatientAppointment.objects.get(pk=id_appointment)
    except patient_models.PatientAppointment.DoesNotExist:
        return JsonResponse(status="404", **context)
    # todo: Code review!!!
    data = {'type': appointment.get_appointment_type_display()}
    if appointment.patient.user.first_name:
        data['name'] = appointment.patient.user.first_name + ' ' \
                       + appointment.patient.user.last_name
    else:
        data['name'] = appointment.patient.user.username
    if appointment.patient.health_complete:
        if appointment.patient.patienthealthhistory.health_conditions:
            data['health_conditions'] = \
                appointment.patient.patienthealthhistory.health_conditions_info
        if appointment.patient.patienthealthhistory.medications:
            data['medications'] = appointment.patient.patienthealthhistory.medications_info
        if appointment.patient.patienthealthhistory.surgeries:
            data['surgeries'] = appointment.patient.patienthealthhistory.surgeries_info
    if appointment.patient.lifestyle_complete:
        data['weight'] = appointment.patient.weight
        data['height_in'] = appointment.patient.height_in
        data['height_ft'] = appointment.patient.height_ft
        data['questions'] = {}
        questions = appointment.patient.patientlifestyle_set.filter(patient=appointment.patient)
        for question in questions:
            if question.answer:
                data['questions'].update({question.question.question_string: 'Yes'})
            else:
                data['questions'].update({question.question.question_string: 'No'})
    if appointment.patient.family_complete:
        data['family'] = {}
        families = appointment.patient.patientfamily_set.filter(patient=appointment.patient)
        for family in families:
            data['family'].update({family.condition.name: family.relationship.name})
    files = appointment.patient.patientfile_set.filter(patient=appointment.patient)
    data['files'] = {}
    for f in files:
        data['files'].update({f.file.name: f.get_type_display})
    data['appointment_id'] = id_appointment
    return data


class AppointmentsView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin,
                       CalendarActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/schedule/appointments.html'
    active_menu_ind = 1
    active_tab_id = 2
    title = _('Appointments')

    def get(self, request, id_appointment=None, status=None, *args, **kwargs):
        context = self.get_context_data()
        if status:
            if id_appointment:
                try:
                    appointment = patient_models.PatientAppointment.objects.get(pk=id_appointment)
                except patient_models.PatientAppointment.DoesNotExist:
                    return Http404(**context)
                appointment.appointment_status = int(status)
                if int(status) == patient_models.PatientAppointment.STATUS_DOCTOR_CANCEL or int(status) == patient_models.PatientAppointment.STATUS_PATIENT_CANCEL:
                    appointment.appointment_time.free = True
                    appointment.appointment_time.save()
                appointment.save()
                return HttpResponseRedirect(redirect_to=reverse_lazy('doctor:appointments'))
            else:
                return Http404(**context)
        elif id_appointment:
            if request.is_ajax():
                return render(request, 'doctor/ajax/patient_details.html',
                              get_appointment_data(id_appointment, context))
        context['appointments'] = patient_models.PatientAppointment.objects.filter(
            doctor=request.user.doctor, appointment_date__appointment_date__gte=datetime.now(),
            appointment_status__gt=patient_models.PatientAppointment.STATUS_EDIT)\
            .order_by('appointment_date', 'appointment_time')
        return super(AppointmentsView, self).get(request, *args, **context)


def gen(start, end, **kwargs):
    cur_date = start
    while cur_date < end:
        cur_date += timedelta(**kwargs)
        yield cur_date


class CalendarView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin,
                   CalendarActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/schedule/calendar.html'
    active_menu_ind = 1
    active_tab_id = 1
    title = _('Calendar')

    def get(self, request, current_date=None, id_time=None, *args, **kwargs):
        if id_time:
            record = doctor_models.DoctorAppointmentTime.objects.get(pk=id_time,
                                                                     appointment_date__doctor=request.user.doctor)
            record.delete()
        now = timezone.now()
        if not current_date:
            current_date = now.strftime('%Y-%m-%d')
        rows = {}
        appointment_date, created = doctor_models.DoctorAppointmentDate.objects.get_or_create(
            doctor=request.user.doctor,
            appointment_date=current_date)
        rows['name'] = current_date
        rows['times'] = doctor_models.DoctorAppointmentTime.objects.filter(
            appointment_date=appointment_date)
        for time in rows['times']:
            if not time.free:
                try:
                    time.appointment = patient_models.PatientAppointment.objects.get(appointment_time_id=time.id)
                except patient_models.PatientAppointment.DoesNotExist:
                    time.free = True
        start_date = datetime(2001, 1, 1, hour=6)
        end_date = datetime(2001, 1, 1, hour=23)
        prev = start_date
        times = []
        exist_times = map(lambda x: x.start_time.strftime('%H:%M'), rows['times'])
        for i in gen(start_date, end_date, minutes=15):
            start_time = prev.strftime('%H:%M')
            if start_time not in exist_times:
                times.append(start_time + '-' + i.strftime('%H:%M'))
            prev = i
        context = self.get_context_data()
        context['times'] = times
        context['current_date'] = current_date
        context['language'] = request.LANGUAGE_CODE
        context['rows'] = rows
        return super(CalendarView, self).get(request, *args, **context)


class TimeView(utils_views.LoginRequiredViewMixin, generic.TemplateView):
    success_url = reverse_lazy('doctor:calendar')
    success_message = _('Time updated')

    def get(self, request, id_appointment_date=None, *args, **kwargs):
        if request.is_ajax:
            data = {}
            appointment_time = doctor_models.DoctorAppointmentTime.objects.filter(
                appointment_date_id=id_appointment_date, free=True)
            for time in appointment_time:
                data[time.id] = time.name
            return JsonResponse(data=data)
        return HttpResponseRedirect(redirect_to=self.success_url)

    def post(self, request, *args, **kwargs):
        appointment_time = request.POST.getlist('appointment_time')
        current_date = request.POST.get('current_date')
        next_url = request.GET.get('next')
        for time in appointment_time:
            arr = time.split('-')
            appointment_date, created = doctor_models.DoctorAppointmentDate.objects.get_or_create(
                doctor=request.user.doctor,
                appointment_date=current_date)
            # todo: add datetime tz support
            obj, created = doctor_models.DoctorAppointmentTime.objects.get_or_create(
                appointment_date=appointment_date,
                start_time=current_date + ' ' + arr[0],
                end_time=current_date + ' ' + arr[1])
            obj.save()
        messages.success(request, self.success_message)
        if next_url:
            return HttpResponseRedirect(redirect_to=next_url)
        return HttpResponseRedirect(redirect_to=self.success_url)


class AppointmentSchedule(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin,
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
                appointment = patient_models.PatientAppointment.objects.get(pk=id_appointment)
            except patient_models.PatientAppointment.DoesNotExist:
                return Http404(**kwargs)
            context = self.get_context_data()
            context['type'] = appointment.get_appointment_type_display()
            context['appointment_id'] = id_appointment
            if appointment.patient.user.first_name:
                context['name'] = appointment.patient.user.first_name + ' ' \
                               + appointment.patient.user.last_name
            else:
                context['name'] = appointment.patient.user.username
            context['appointment_date'] = appointment.appointment_date
            context['appointment_time'] = appointment.appointment_time
            context['dates'] = doctor_models.DoctorAppointmentDate.objects.filter(
                doctor=request.user.doctor, appointment_date__gte=datetime.now()).order_by('appointment_date')
            context['times'] = doctor_models.DoctorAppointmentTime.objects.filter(
                appointment_date_id=appointment.appointment_date_id, free=True)
            return super(AppointmentSchedule, self).get(request, *args, **context)
        if next_url:
            return HttpResponseRedirect(redirect_to=next_url)
        return HttpResponseRedirect(redirect_to=self.success_url)

    def post(self, request, id_appointment=None, *args, **kwargs):
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        next_url = request.GET.get('next')
        if appointment_date:
            if appointment_time:
                try:
                    appointment = patient_models.PatientAppointment.objects.get(pk=id_appointment)
                except patient_models.PatientAppointment.DoesNotExist:
                    return Http404(**kwargs)

                try:
                    appointment.appointment_date = doctor_models.DoctorAppointmentDate.objects.get(pk=appointment_date)
                except doctor_models.DoctorAppointmentDate.DoesNotExist:
                    return Http404(**kwargs)
                try:
                    new_time = doctor_models.DoctorAppointmentTime.objects.get(pk=appointment_time)
                    new_time.free = False
                    new_time.save()
                    appointment.appointment_time.free = True
                    appointment.appointment_time.save()
                    appointment.appointment_time = new_time
                except doctor_models.DoctorAppointmentTime.DoesNotExist:
                    return Http404(**kwargs)
                appointment.appointment_status = patient_models.PatientAppointment.STATUS_DOCTOR_RESCHEDULE
                appointment.save()
                messages.success(request, self.success_message)
                if next_url:
                    return HttpResponseRedirect(redirect_to=next_url)
                return HttpResponseRedirect(redirect_to=self.success_url)
        return Http404(**kwargs)


class CaseListView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, CaseActiveTabMixin, generic.ListView):
    template_name = 'doctor/case/case_list.html'
    active_menu_ind = 2
    active_tab_id = 1
    title = _('Open case')
    type = 'open'
    success_url = reverse_lazy('doctor:case', kwargs={'type': type})
    paginate_by = 20

    def get_queryset(self):
        if self.type == 'open':
            return patient_models.PatientCase.objects.filter(doctor=self.request.user.doctor).order_by('updated_date')
        return patient_models.PatientCase.objects.filter(doctor=self.request.user.doctor, closed=True)\
            .order_by('updated_date')

    def get_context_data(self, **kwargs):
        context = super(CaseListView, self).get_context_data(**kwargs)
        context['type'] = self.type
        return context

    def get(self, request, type=None, *args, **kwargs):
        self.type = type
        if type == 'close':
            self.active_tab_id = 2
        return super(CaseListView, self).get(request, *args, **kwargs)


class CaseView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, CaseActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/case/case.html'
    active_menu_ind = 2
    active_tab_id = 1
    title = _('Create case')
    success_url = 'doctor:edit_case'

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
        context['reasons'] = utils_models.AppointmentReason.objects.all()
        # context['appointments'] = patient_models.PatientAppointment.objects.filter(case__in=[None, case])
        # if id_test:
        #     test = patient_models.Test.objects.get(pk=id_test)
        #     test.delete()
        #     return HttpResponseRedirect(redirect_to=reverse_lazy('doctor:view_case', kwargs={'id_case': case.id},))
        #
        return self.render_to_response(context=context)

    def post(self, request, id_case=None, *args, **kwargs):
        reason = utils_models.AppointmentReason.objects.get(pk=request.POST.get('reason'))
        patient = patient_models.Patient.objects.get(pk=request.POST.get('patient'))
        case = patient_models.PatientCase(doctor=request.user.doctor, patient=patient, reason=reason)
        case.save()
        print case
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
        return HttpResponseRedirect(redirect_to=reverse_lazy(self.success_url, kwargs={'id_case': case.id}))


class EditCaseView(utils_views.LoginRequiredViewMixin, DoctorMenuViewMixin, CaseActiveTabMixin, generic.TemplateView):
    template_name = 'doctor/case/edit_case.html'
    active_menu_ind = 2
    active_tab_id = 1
    title = _('Edit case')
    success_url = 'doctor:edit_case'

    def get(self,  request, id_case=None, *args, **kwargs):

        context = self.get_context_data()
        case = patient_models.PatientCase.objects.get(pk=id_case)
        context['patients'] = patient_models.Patient.objects.all()
        context['reasons'] = utils_models.AppointmentReason.objects.all()
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


        print id_case
        return self.render_to_response(context=context)



