import json
from allauth.account.views import PasswordChangeView
import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from patient import models, forms as patient_forms
from utils import models as util_models, forms as utils_forms
from utils.views import LoginRequiredViewMixin, PasswordChangeTemplateMixin
from doctor import models as doctor_models
from utils import views as utils_views
from doctor import views as doctor_views
from django.utils.dateparse import parse_datetime


class PatientMenuViewMixin(utils_views.MenuViewMixin):
    options = [
        {'class': 'fa-bar-chart-o', 'title': _('Dashboard'),
         'href': reverse_lazy('patient:dashboard')},
        {'class': 'fa-user', 'title': _('Talk to a doctor'),
         'href': reverse_lazy('patient:talk_to_a_doctor')},
        {'class': 'fa-heart', 'title': _('My health'),
         'href': reverse_lazy('patient:my_health_history')},
        {'class': 'fa-envelope', 'title': _('Message Center'),
         'href': reverse_lazy('patient:messages')},
        {'class': 'fa-support', 'title': _('Help & Support'),
         'href': reverse_lazy('patient:help')},
    ]


class PatientActiveTabMixin(utils_views.ActiveTabMixin):
    tabs = [
        {'title': _('My Health History'),
         'href': reverse_lazy('patient:my_health_history')},
        {'title': _('My Lifestyle'),
         'href': reverse_lazy('patient:my_lifestyle')},
        {'title': _('My Family History'),
         'href': reverse_lazy('patient:my_family_history')},
    ]

    process = [
        {'title': _('Choose Provider'),
         'number': 1,
         'href': reverse_lazy('patient:talk_to_a_doctor'),
         'finished': False,},
        {'title': _('Medical History'),
         'number': 2,
         'href': reverse_lazy('patient:my_health_history'),
         'finished': False,},
        {'title': _('Payment'),
         'number': 3,
         'href': reverse_lazy('patient:billing'),
         'finished': False,},
        {'title': _('Confirmation'),
         'number': 4,
         'href': reverse_lazy('patient:confirmation'),
         'finished': False,}
    ]


class DashboardView(LoginRequiredViewMixin, PatientMenuViewMixin, generic.TemplateView):
    active_menu_ind = 0
    template_name = 'patient/dashboard.html'
    title = _('Dashboard')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['doctors'] = doctor_models.Doctor.objects.all().exclude(
            user__first_name='', user__last_name='')
        context['specialties'] = util_models.Specialty.objects.all()
        return self.render_to_response(context)


class TalkToADoctor(LoginRequiredViewMixin, PatientMenuViewMixin, PatientActiveTabMixin, generic.ListView):
    model = doctor_models.Doctor
    template_name = 'patient/dashboard/talk_to_a_doctor.html'
    context_object_name = 'doctors'
    active_menu_ind = 1
    title = _('Talk to a doctor')
    active_proc = 1

    def get_queryset(self):
        query = super(TalkToADoctor, self).get_queryset()
        query = query.exclude(user__first_name='', user__last_name='')

        doctor_specialty = self.request.GET.get('doctor_specialty', None)
        doctor = self.request.GET.get('doctor', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        current_timezone = timezone.get_current_timezone()
        if start_date:
            start_date = current_timezone.localize(datetime.datetime.strptime(start_date, "%m/%d/%Y"))
            query = query.filter(doctorappointmenttime__start_time__gte=start_date)
        if end_date:
            end_date = current_timezone.localize(datetime.datetime.strptime(end_date, "%m/%d/%Y"))
            query = query.filter(doctorappointmenttime__start_time__lte=end_date)
        if doctor_specialty:
            query = query.filter(doctorspecialty__specialty=doctor_specialty)
        if doctor:
            query = query.filter(id=doctor)
        else:
            query = query.distinct('id')
        return query

    def get_context_data(self, **kwargs):
        context = super(TalkToADoctor, self).get_context_data(**kwargs)
        context['specialties'] = util_models.Specialty.objects.all()
        context['all_doctors'] = doctor_models.Doctor.objects.all().exclude(
            user__first_name='', user__last_name='')
        chosen_specialty = self.request.GET.get('doctor_specialty')
        chosen_doctor = self.request.GET.get('doctor')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        if chosen_specialty:
            chosen_specialty = int(chosen_specialty)
        context['chosen_specialty'] = chosen_specialty
        if chosen_doctor:
            chosen_doctor = int(chosen_doctor)
        context['chosen_doctor'] = chosen_doctor

        context['start_date'] = start_date

        context['end_date'] = end_date
        return context


class MyHealth(LoginRequiredViewMixin, PatientMenuViewMixin, PatientActiveTabMixin, generic.FormView):
    active_menu_ind = 2
    title = _('My health')
    active_tab_id = 1
    active_proc = 2


class MyHealthHistory(MyHealth):
    template_name = 'patient/dashboard/my_health/my_health_history.html'
    form_class = patient_forms.HealthHistoryForm
    success_url = reverse_lazy('patient:my_health_history')
    title = _('My Health History')
    active_tab_id = 1
    success_message = _('My health records updated')

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        try:
            health_history = models.PatientHealthHistory.objects.get(patient=self.request.user.patient)
            return form_class(instance=health_history, **self.get_form_kwargs())
        except models.PatientHealthHistory.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        form.save()
        self.request.user.patient.health_complete = True
        self.request.user.patient.save()
        return super(MyHealthHistory, self).form_valid(form)


class MyRecords(MyHealth):
    template_name = 'patient/dashboard/my_health/my_records.html'
    form_class = patient_forms.MyRecordsForm
    success_url = reverse_lazy('patient:my_records')
    success_message = _('Records updated')

    def get(self, request, id_file=None, *args, **kwargs):
        if id_file:
            record = models.PatientFile.objects.get(pk=id_file, patient=request.user.patient)
            record.delete()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form,
                                                             files=models.PatientFile.objects.filter(
                                                                 patient=request.user.patient)))

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        form.save()
        return super(MyRecords, self).form_valid(form)


class MyLifestyle(MyHealth):
    template_name = 'patient/dashboard/my_health/my_lifestyle.html'
    form_class = patient_forms.LifestyleForm
    success_url = reverse_lazy('patient:my_lifestyle')
    title = 'My Life Style'
    active_tab_id = 2
    success_message = _('Lifestyle information updated')

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        data = {'patient_id': self.request.user.patient.id,
                'height_ft': self.request.user.patient.height_ft,
                'height_in': self.request.user.patient.height_in,
                'weight': self.request.user.patient.weight}
        try:
            question_answers = models.PatientLifestyle.objects.filter(patient=self.request.user.patient)
            for q_answer in question_answers:
                data['question_%s' % q_answer.question_id] = q_answer.answer
        except models.PatientLifestyle.DoesNotExist:
            pass
        kw = self.get_form_kwargs()
        kw['initial'].update(data)
        return form_class(**kw)

    def form_valid(self, form):
        self.request.user.patient.height_ft = form.cleaned_data['height_ft']
        self.request.user.patient.height_in = form.cleaned_data['height_in']
        self.request.user.patient.weight = form.cleaned_data['weight']
        self.request.user.patient.save()
        questions = models.PatientLifestyleQuestion.objects.all()
        for question in questions:
            try:
                q_answer = models.PatientLifestyle.objects.get(patient=self.request.user.patient, question=question)
            except models.PatientLifestyle.DoesNotExist:
                q_answer = models.PatientLifestyle(patient=self.request.user.patient, question=question)
            q_answer.answer = form.cleaned_data['question_%s' % question.id]
            q_answer.save()
        self.request.user.patient.lifestyle_complete = True
        self.request.user.patient.save()
        return super(MyLifestyle, self).form_valid(form)


class MyFamilyHistory(MyHealth):
    template_name = 'patient/dashboard/my_health/my_family_history.html'
    form_class = patient_forms.FamilyHistoryForm
    success_url = reverse_lazy('patient:my_family_history')
    title = _('My Family History')
    active_tab_id = 3
    success_message = _('Family history updated')

    def __init__(self):
        super(MyFamilyHistory, self).__init__()

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kw = self.get_form_kwargs()
        kw['initial'].update({'patient_id': self.request.user.patient.id})
        data = {}
        conditions = models.PatientFamilyCondition.objects.filter(Q(patient_id=self.request.user.patient.id) |
                                                                  Q(patient_id=None))
        for condition in conditions:
            try:
                data['condition_%s' % condition.id] = models.PatientFamily.objects.get(
                                                                condition=condition,
                                                                patient=self.request.user.patient).relationship_id
            except models.PatientFamily.DoesNotExist:
                pass
        kw['initial'].update(data)
        return form_class(**kw)

    def form_valid(self, form):
        conditions = models.PatientFamilyCondition.objects.filter(Q(patient_id=self.request.user.patient.id) |
                                                                  Q(patient_id=None))
        for condition in conditions:
            if form.cleaned_data['condition_%s' % condition.id]:
                try:
                    relation = models.PatientFamily.objects.get(condition=condition, patient=self.request.user.patient)
                except models.PatientFamily.DoesNotExist:
                    relation = models.PatientFamily(condition=condition, patient=self.request.user.patient)
                relation.relationship = form.cleaned_data['condition_%s' % condition.id]
                relation.save()
        self.request.user.patient.family_complete = True
        self.request.user.patient.save()
        return super(MyFamilyHistory, self).form_valid(form)


class MessageCenter(LoginRequiredViewMixin, PatientMenuViewMixin, generic.TemplateView):
    template_name = 'patient/dashboard/message_center.html'
    active_menu_ind = 3
    title = _('Message Center')


class HelpSupport(LoginRequiredViewMixin, PatientMenuViewMixin, generic.TemplateView):
    template_name = 'patient/dashboard/help_support.html'
    active_menu_ind = 4
    title = _('Help')


class MyAccountBaseView(LoginRequiredViewMixin, PatientMenuViewMixin, utils_views.ActiveTabMixin):
    tabs = [
        {'img': 'img/my_account.png',
         'href': reverse_lazy('patient:my_account'),
         'header': _('Account Details'),
         },
        {'img': 'img/billing.jpg',
         'href': reverse_lazy('patient:billing'),
         'header': _('Billing information'),
         },
        {'img': 'img/change_password.png',
         'href': reverse_lazy('patient:password'),
         'header': _('Login & Password'),
         },
        {'img': 'img/activity.png',
         'href': reverse_lazy('patient:history'),
         'header': _('Account history'),
         },
    ]


class HistoryView(MyAccountBaseView, generic.TemplateView):
    template_name = 'patient/account/history.html'
    title = _('My Account')
    active_tab_id = 4

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['history_records'] = models.PatientHistory.objects.filter(patient=request.user.patient)
        return self.render_to_response(context)


class PasswordView(MyAccountBaseView, PasswordChangeTemplateMixin, PasswordChangeView):
    success_url = reverse_lazy("patient:password")
    form_class = utils_forms.MyChangePassForm
    active_tab_id = 3
    title = _('Change Password')


class BillingView(MyAccountBaseView, PatientActiveTabMixin, generic.FormView):
    template_name = 'patient/account/billing.html'
    form_class = patient_forms.BillingForm
    success_url = reverse_lazy('patient:billing')
    active_tab_id = 2
    title = _('Billing Information')
    success_message = _('Billing information updated')
    active_proc = 3

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        try:
            billing_info = models.PatientBilling.objects.get(patient=self.request.user.patient)
            return form_class(instance=billing_info, **self.get_form_kwargs())
        except models.PatientBilling.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        form.save()
        self.request.user.patient.billing_complete = True
        self.request.user.patient.save()
        return super(BillingView, self).form_valid(form)


class DetailsView(MyAccountBaseView, generic.TemplateView):
    template_name = 'patient/account/details.html'
    active_tab_id = 1
    title = _('Account Details')
    success_message = _('Account details updated')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user_form'] = utils_forms.DetailUserForm(instance=request.user)
        context['detail_form'] = patient_forms.DetailForm(instance=request.user.patient)
        return super(DetailsView, self).get(request, *args, **context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_form = utils_forms.DetailUserForm(request.POST, instance=request.user)
        detail_form = patient_forms.DetailForm(request.POST, request.FILES, instance=request.user.patient)
        if user_form.is_valid() and detail_form.is_valid():
            user_form.save()
            detail_form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(redirect_to=reverse_lazy('patient:my_account'))
        context['user_form'] = user_form
        context['detail_form'] = detail_form
        return render(request, self.template_name, context)


class DoctorDetailView(LoginRequiredViewMixin, generic.DetailView):
    model = doctor_models.Doctor
    template_name = 'patient/dashboard/doctor_info.html'

    def get_context_data(self, **kwargs):
        data = super(DoctorDetailView, self).get_context_data(**kwargs)
        query = doctor_models.DoctorAppointmentTime.objects.filter(
                doctor=self.object, start_time__gte=timezone.now().date(), free=True)
        data['appointment_time'] = query
        return data


class PatientAppointmentProcessView(PatientActiveTabMixin, generic.View):

    def get(self, *args, **kwargs):
        next_url = ''
        patient = self.request.user.patient
        if not patient.patientappointment_set.filter(appointment_status=models.PatientAppointment.STATUS_EDIT).exists():
            next_url = reverse_lazy('patient:talk_to_a_doctor')
        elif not patient.health_complete:
            next_url = reverse_lazy('patient:my_health_history')
        elif not patient.lifestyle_complete:
            next_url = reverse_lazy('patient:my_lifestyle')
        elif not patient.family_complete:
            next_url = reverse_lazy('patient:my_family_history')
        elif not patient.billing_complete:
            next_url = reverse_lazy('patient:billing')
        else:
            next_url = reverse_lazy('patient:confirmation')
        next_url += '?app_process=true'
        return HttpResponseRedirect(next_url)


class PatientAppointmentView(generic.FormView):
    template_name = 'patient/appointment_request.html'
    form_class = patient_forms.PatientAppointmentForm
    success_url = reverse_lazy('patient:appointment_process')

    def get_initial(self):
        initial = super(PatientAppointmentView, self).get_initial()

        initial['patient'] = self.request.user.patient
        time = models.DoctorAppointmentTime.objects.get(pk=self.kwargs.get('pk'))
        initial['appointment_time'] = time
        # initial['appointment_date'] = time.appointment_date
        initial['doctor'] = time.doctor
        return initial

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'success': True,
                            'url': self.get_success_url()})

    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        })


class ConfirmAppointmentProcessView(PatientMenuViewMixin, PatientActiveTabMixin, generic.TemplateView):
    template_name = 'patient/confirmation.html'
    active_menu_ind = 1
    title = _('Confirmation')
    active_proc = 4
    success_message = _('New appointment created')

    def get_context_data(self, **kwargs):
        context = super(ConfirmAppointmentProcessView, self).get_context_data(**kwargs)
        pk = self.request.user.patient.patientappointment_set.order_by('id').last().pk
        data = doctor_views.get_appointment_data(pk, context)
        context['taken'] = False
        context.update(data)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        appointment = models.PatientAppointment.objects.get(pk=context['appointment_id'])
        if appointment.appointment_time.free:
            messages.success(request, self.success_message)
            appointment.appointment_time.free = False
            appointment.appointment_status = models.PatientAppointment.STATUS_NEW
            appointment.appointment_time.save()
            appointment.save()
            context['error'] = False
            context['taken'] = True
        else:
            context['error'] = True
            context['taken'] = True
        return render(request, self.template_name, context)


class ConsultationView(LoginRequiredViewMixin, PatientMenuViewMixin, PatientActiveTabMixin, generic.TemplateView):
    active_menu_ind = 2
    template_name = 'patient/dashboard/my_health/consultation.html'
    title = _('Consultation History')
    success_message = _('Consultation updated')
    active_tab_id = 2

    def get(self, request, id_appointment=None, status=None, *args, **kwargs):
        context = self.get_context_data()
        if status:
            if id_appointment:
                try:
                    appointment = models.PatientAppointment.objects.get(pk=id_appointment)
                except models.PatientAppointment.DoesNotExist:
                    return Http404(**context)
                appointment.appointment_status = status
                if status == models.PatientAppointment.STATUS_DOCTOR_CANCEL or status == models.PatientAppointment.STATUS_PATIENT_CANCEL:
                    appointment.appointment_time.free = True
                    appointment.appointment_time.save()
                appointment.save()
                return HttpResponseRedirect(redirect_to=reverse_lazy('patient:consultation'))
            else:
                return Http404(**context)
        context['appointments'] = models.PatientAppointment.objects.filter(
            patient=request.user.patient, appointment_time__start_time__gte=timezone.now().date())\
            .order_by('appointment_time')
        return super(ConsultationView, self).get(request, *args, **context)


class ConsultationEdit(utils_views.LoginRequiredViewMixin, PatientMenuViewMixin,
                       PatientActiveTabMixin, generic.FormView):
    template_name = 'patient/dashboard/my_health/consultation_edit.html'
    form_class = patient_forms.PatientConsultationForm
    success_url = reverse_lazy('patient:consultation')

    def get_form_kwargs(self):
        kwargs = super(ConsultationEdit, self).get_form_kwargs()
        instance = models.PatientAppointment.objects.get(pk=self.kwargs.get('pk'))
        kwargs.update({'instance': instance})
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(ConsultationEdit, self).form_valid(form)


def get_all_doctors_json(request):
    query = doctor_models.Doctor.objects.exclude(user__first_name='', user__last_name='')
    data = []
    for doctor in query:
        data.append({
            'id': doctor.id,
            'text': str(doctor)
        })
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')


def get_doctor_appointment_time(request):
    pk = request.GET.get('appointment_date')
    data = {'': 'Select'}
    if pk:
        query = doctor_models.DoctorAppointmentDate.objects.get(
            pk=pk).doctorappointmenttime_set.filter(free=True)
        if query:
            for date in query:
                data.update({date.pk: date.name})
        else:
            data = {'': "Don't have time"}
    return JsonResponse(data)
