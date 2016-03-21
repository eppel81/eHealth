from itertools import chain
import json
import datetime
import braintree
from allauth.account.views import PasswordChangeView
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, \
    Http404
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from postman import views as postman_views
from postman import models as postman_models
from postman.forms import AnonymousWriteForm
from postman.models import Message
from django.conf import settings

from utils import models as util_models, forms as utils_forms
from utils import views as utils_views
from utils.views import PatientMixin, PasswordChangeTemplateMixin, \
    PatientMixin, LoginRequiredMixin
from utils.views import get_appointment_room_availability
from doctor import models as doctor_models
from doctor import views as doctor_views
from patient import models, forms as patient_forms


class PatientMenuViewMixin(utils_views.MenuViewMixin):
    options = [
        {'class': 'fa-bar-chart-o', 'title': _('Dashboard'),
         'href': reverse_lazy('patient:dashboard')},
        {'class': 'fa-user', 'title': _('Talk to a doctor'),
         'href': reverse_lazy('patient:talk_to_a_doctor')},
        {'class': 'fa-heart', 'title': _('My health'),
         'href': reverse_lazy('patient:my_health_history')},
        {'class': 'fa-envelope', 'title': _('Message Center'),
         'href': reverse_lazy('patient:inbox'), 'check_messages': True},
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

    base_tabs = [
        {'title': _('My Medical Profile'),
         'href': reverse_lazy('patient:my_health_history'),
         'icon': 'img/my_health.jpg'},
        {'title': _('Consultation History'),
         'href': reverse_lazy('patient:consultation'),
         'icon': 'img/consultation.png', },
        {'title': _('My Medical Records'),
         'href': reverse_lazy('patient:my_records'),
         'icon': 'img/folder.png', },
        {'title': _('My Cases'),
         'href': reverse_lazy('patient:all_cases', kwargs={'type': 'open'}),
         'icon': 'img/cases.jpg', }
    ]

    process = [
        {'title': _('My Health History'),
         'number': 1,
         'href': reverse_lazy('patient:my_health_history'),
         'finished': False, },
        {'title': _('My Lifestyle'),
         'number': 2,
         'href': reverse_lazy('patient:my_lifestyle'),
         'finished': False, },
        {'title': _('My Family History'),
         'number': 3,
         'href': reverse_lazy('patient:my_family_history'),
         'finished': False, },
        {'title': _('Confirmation'),
         'number': 4,
         'href': reverse_lazy('patient:confirmation'),
         'finished': False, },
    ]

    process1 = [
        {'title': _('My Health History'),
         'number': 1,
         'href': reverse_lazy('patient:health_history_proc'),
         'finished': False, },
        {'title': _('My Lifestyle'),
         'number': 2,
         'href': reverse_lazy('patient:lifestyle_proc'),
         'finished': False, },
        {'title': _('My Family History'),
         'number': 3,
         'href': reverse_lazy('patient:family_history_proc'),
         'finished': False, },
        {'title': _('Confirmation'),
         'number': 4,
         'href': reverse_lazy('patient:confirm'),
         'finished': False, },
    ]

    message_tabs = [
        {'class': 'message_in',
         'href': reverse_lazy('patient:inbox'),
         'title': _('Inbox'),
         },
        {'class': 'message_out',
         'href': reverse_lazy('patient:sent'),
         'title': _('Sent'),
         },
        {'class': 'message_lock',
         'href': reverse_lazy('patient:archives'),
         'title': _('Archived'),
         },
        {'class': 'message_ban',
         'href': reverse_lazy('patient:trash'),
         'title': _('Deleted'),
         },
        {'class': 'pen',
         'href': reverse_lazy('patient:write_message_doctor'),
         'title': _('Send new message to'),
         },
    ]


class DashboardView(PatientMixin, PatientMenuViewMixin,
                    generic.TemplateView):
    active_menu_ind = 0
    template_name = 'patient/dashboard.html'
    title = _('Dashboard')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['doctors'] = doctor_models.Doctor.objects.all().exclude(
            user__first_name='', user__last_name='')
        context['specialties'] = util_models.Specialty.objects.all()
        appointments_status = [
            models.PatientAppointment.STATUS_EDIT,
            models.PatientAppointment.STATUS_NEW,
            models.PatientAppointment.STATUS_DOCTOR_APPROVE,
            models.PatientAppointment.STATUS_PATIENT_RESCHEDULE,
        ]
        current_appointments = models.PatientAppointment.objects.filter(
                case__patient=self.request.user.patient,
                appointment_status__in=appointments_status)
        today = timezone.now()
        for appointment in current_appointments:
            start_time = appointment.appointment_time.start_time
            duration = appointment.appointment_time.duration
            delta = start_time + datetime.timedelta(minutes=duration)
            if start_time <= today <= delta and appointment.appointment_status==models.PatientAppointment.STATUS_DOCTOR_APPROVE:
                today = start_time
        current_appointments = current_appointments.filter(appointment_time__start_time__gte=today)
        context['current_appointments'] = current_appointments
        context['appointment_availability'] = get_appointment_room_availability(current_appointments)

        return self.render_to_response(context)


class TalkToADoctor(PatientMixin, PatientMenuViewMixin,
                    PatientActiveTabMixin, generic.ListView):
    model = doctor_models.Doctor
    template_name = 'patient/dashboard/talk_to_a_doctor.html'
    context_object_name = 'doctors'
    active_menu_ind = 1
    title = _('Talk to a doctor')

    def get_queryset(self):
        self.process1[0]['finished'] = True if \
            self.request.user.patient.health_complete else False
        self.process1[1]['finished'] = True if \
            self.request.user.patient.lifestyle_complete else False
        self.process1[2]['finished'] = True if \
            self.request.user.patient.family_complete else False

        query = super(TalkToADoctor, self).get_queryset()
        query = query.exclude(user__first_name='', user__last_name='')
        doctor = self.request.GET.get('doctor', None)
        doctor_specialty = self.request.GET.get('doctor_specialty', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        doctor_specialty_now = self.request.GET.get('doctor_specialty_now', None)

        if 'find_doctor' in self.request.GET:
            current_timezone = timezone.get_current_timezone()
            if start_date:
                start_date = current_timezone.localize(
                    datetime.datetime.strptime(start_date, "%m/%d/%Y"))
                query = query.filter(
                    doctorappointmenttime__start_time__gte=start_date)
            if end_date:
                end_date = current_timezone.localize(
                    datetime.datetime.strptime(end_date, "%m/%d/%Y"))
                query = query.filter(
                    doctorappointmenttime__start_time__lte=end_date)
            if doctor_specialty:
                query = query.filter(doctorspecialty__specialty=doctor_specialty)
        elif 'find_doctor_now' in self.request.GET:
            now = timezone.now()
            hour_delta = now + datetime.timedelta(minutes=60)
            query = query.filter(doctorappointmenttime__start_time__gte=now,
                                 doctorappointmenttime__start_time__lte=hour_delta)
            if doctor_specialty_now:
                query = query.filter(doctorspecialty__specialty=doctor_specialty_now)

        elif 'find_one_doctor' in self.request.GET:
            if doctor:
                query = query.filter(id=doctor)
        if not doctor:
            query = query.order_by('id').distinct()

        # consult rate filtering
        consult_rate_start = self.request.GET.get('slider_rate_value1', None)
        consult_rate_end = self.request.GET.get('slider_rate_value2', None)
        if consult_rate_start:
            query = query.filter(consult_rate__gte=consult_rate_start)
        if consult_rate_end and consult_rate_end > consult_rate_start:
            query = query.filter(consult_rate__lte=consult_rate_end)

        return query

    def get_context_data(self, **kwargs):
        context = super(TalkToADoctor, self).get_context_data(**kwargs)
        context['specialties'] = util_models.Specialty.objects.all()
        context['all_doctors'] = doctor_models.Doctor.objects.all().exclude(
            user__first_name='', user__last_name='')
        doctor_specialty = self.request.GET.get('doctor_specialty')
        doctor_specialty_now = self.request.GET.get('doctor_specialty_now')
        chosen_doctor = self.request.GET.get('doctor')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')

        if 'find_doctor' in self.request.GET:
            if doctor_specialty:
                context['doctor_specialty'] = int(doctor_specialty)
            context['start_date'] = start_date
            context['end_date'] = end_date

        elif 'find_doctor_now' in self.request.GET:
            if doctor_specialty_now:
                context['doctor_specialty_now'] = int(doctor_specialty_now)

        elif 'find_one_doctor' in self.request.GET:
            if chosen_doctor:
                context['chosen_doctor'] = int(chosen_doctor)

        #consult rate slider context
        consult_rate_start = self.request.GET.get('slider_rate_value1', '')
        consult_rate_end = self.request.GET.get('slider_rate_value2', '')
        if consult_rate_start:
            consult_rate_start = int(consult_rate_start)
        context['consult_rate_start'] = consult_rate_start
        if consult_rate_end:
            consult_rate_end = int(consult_rate_end)
        context['consult_rate_end'] = consult_rate_end if \
            consult_rate_end >= consult_rate_start else ''

        context['process1'][0]['finished'] = True if \
            self.request.user.patient.health_complete else False
        context['process1'][1]['finished'] = True if \
            self.request.user.patient.lifestyle_complete else False
        context['process1'][2]['finished'] = True if \
            self.request.user.patient.family_complete else False
        return context


class MyHealth(PatientMixin, PatientMenuViewMixin,
               PatientActiveTabMixin, generic.FormView):
    active_menu_ind = 2
    title = _('My health')
    active_tab_id = 1
    base_active_tab = 1

    def get_context_data(self, **kwargs):
        context = super(MyHealth, self).get_context_data(**kwargs)
        context['process1'][0]['finished'] = True \
            if self.request.user.patient.health_complete else False

        context['process1'][1]['finished'] = True \
            if self.request.user.patient.lifestyle_complete else False

        context['process1'][2]['finished'] = True \
            if self.request.user.patient.family_complete else False

        context['old_process'] = True

        return context


class MyHealthHistory(MyHealth):
    template_name = 'patient/dashboard/my_health/my_health_history.html'
    form_class = patient_forms.HealthHistoryForm
    success_url = reverse_lazy('patient:my_health_history')
    title = _('My Health History')
    active_tab_id = 1
    active_proc = 1
    success_message = _('My health records updated')

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        pk = self.request.GET.get('pk', None)
        if next_url:
            if pk:
                return str(next_url + '?pk=' + pk)
            return next_url
        else:
            if pk:
                return str(self.success_url + '?pk=' + pk)
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        try:
            health_history = models.PatientHealthHistory.objects.get(
                patient=self.request.user.patient)
            return form_class(instance=health_history, **self.get_form_kwargs())
        except models.PatientHealthHistory.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        form.save()
        self.request.user.patient.health_complete = True
        self.request.user.patient.save()
        return super(MyHealthHistory, self).form_valid(form)


class MyRecords(PatientActiveTabMixin, PatientMixin, PatientMenuViewMixin,
                generic.ListView):
    template_name = 'patient/dashboard/my_health/my_records.html'
    success_url = reverse_lazy('patient:my_records')
    success_message = _('Records updated')
    base_active_tab = 3
    active_menu_ind = 2
    context_object_name = 'files'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MyRecords, self).get_context_data(**kwargs)
        model = models.TestFileRecord
        context['types'] = {
            model.TEST: model.STATUS_CHOICES[model.TEST][1],
            model.RECORD: model.STATUS_CHOICES[model.RECORD][1]
        }

        return context

    def get_queryset(self):
        query = models.TestFileRecord.objects.filter(
            case__patient=self.request.user.patient)
        record_type = self.request.GET.get('type')
        if record_type:
            record_type = int(record_type)
            query = query.filter(type=record_type)
        search_query = self.request.GET.get('search')
        if search_query:
            query = query.filter(Q(description__icontains=search_query) |
                                 Q(conclusions__icontains=search_query) |
                                 Q(requested_by__icontains=search_query) |
                                 Q(completed_by__icontains=search_query)
                                 )
        return query


class MyLifestyle(MyHealth):
    template_name = 'patient/dashboard/my_health/my_lifestyle.html'
    form_class = patient_forms.LifestyleForm
    success_url = reverse_lazy('patient:my_lifestyle')
    title = _('My Life Style')
    active_tab_id = 2
    active_proc = 2
    success_message = _('Lifestyle information updated')

    def get_context_data(self, **kwargs):
        context = super(MyLifestyle, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        pk = self.request.GET.get('pk', None)
        if next_url:
            if pk:
                return str(next_url + '?pk=' + pk)
            return next_url
        else:
            if pk:
                return str(self.success_url + '?pk=' + pk)
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        data = {'patient_id': self.request.user.patient.id,
                'height_ft': self.request.user.patient.height_ft,
                'height_in': self.request.user.patient.height_in,
                'weight': self.request.user.patient.weight}
        try:
            question_answers = models.PatientLifestyle.objects.filter(
                patient=self.request.user.patient)
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
                q_answer = models.PatientLifestyle.objects.get(
                    patient=self.request.user.patient, question=question)
            except models.PatientLifestyle.DoesNotExist:
                q_answer = models.PatientLifestyle(
                    patient=self.request.user.patient, question=question)
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
    active_proc = 3
    success_message = _('Family history updated')

    def get_context_data(self, **kwargs):
        context = super(MyFamilyHistory, self).get_context_data(**kwargs)

        return context

    def __init__(self):
        super(MyFamilyHistory, self).__init__()

    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        pk = self.request.GET.get('pk', None)
        if next_url:
            if pk:
                return str(next_url + '?pk=' + pk)
            return next_url
        else:
            if pk:
                return str(self.success_url + '?pk=' + pk)
            return self.success_url

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kw = self.get_form_kwargs()
        kw['initial'].update({'patient_id': self.request.user.patient.id})
        data = {}
        conditions = models.PatientFamilyCondition.objects.filter(
            Q(patient_id=self.request.user.patient.id) |
            Q(patient_id=None))
        for condition in conditions:
            try:
                data[
                    'condition_%s' % condition.id] = \
                    models.PatientFamily.objects.get(
                        condition=condition,
                        patient=self.request.user.patient).relationship_id
            except models.PatientFamily.DoesNotExist:
                pass
        kw['initial'].update(data)
        return form_class(**kw)

    def form_valid(self, form):
        conditions = models.PatientFamilyCondition.objects.filter(
            Q(patient_id=self.request.user.patient.id) |
            Q(patient_id=None))
        for condition in conditions:
            if form.cleaned_data['condition_%s' % condition.id]:
                try:
                    relation = models.PatientFamily.objects.get(
                        condition=condition, patient=self.request.user.patient)
                except models.PatientFamily.DoesNotExist:
                    relation = models.PatientFamily(
                        condition=condition,
                        patient=self.request.user.patient)
                relation.relationship = form.cleaned_data[
                    'condition_%s' % condition.id]
                relation.save()
        self.request.user.patient.family_complete = True
        self.request.user.patient.save()
        return super(MyFamilyHistory, self).form_valid(form)


class MessageFolderMixin(object):
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


class InboxMessagesView(PatientMixin, PatientMenuViewMixin,
                        PatientActiveTabMixin,
                        MessageFolderMixin, postman_views.InboxView):
    active_menu_ind = 3
    message_active_tab = 1


class SentMessagesView(PatientMixin, PatientMenuViewMixin,
                       PatientActiveTabMixin,
                       MessageFolderMixin, postman_views.SentView):
    active_menu_ind = 3
    message_active_tab = 2


class ArchivedMessagesView(PatientMixin, PatientMenuViewMixin,
                           PatientActiveTabMixin,
                           MessageFolderMixin, postman_views.ArchivesView):
    active_menu_ind = 3
    message_active_tab = 3


class DeletedMessagesView(PatientMixin, PatientMenuViewMixin,
                          PatientActiveTabMixin,
                          MessageFolderMixin, postman_views.TrashView):
    active_menu_ind = 3
    message_active_tab = 4


class ShowMessageView(LoginRequiredMixin, postman_views.MessageView):
    template_name = 'postman/message_view.html'


class ShowConversationView(LoginRequiredMixin, postman_views.ConversationView):
    template_name = 'postman/message_view.html'


class WriteMessageMixin(PatientMixin, PatientMenuViewMixin,
                        PatientActiveTabMixin):
    write_message_tabs = []
    write_message_active_tab = 0
    active_menu_ind = 3
    message_active_tab = 5

    def get_active_write_message_tab(self):
        return self.write_message_tabs[self.write_message_active_tab - 1]

    def get_context_data(self, **kwargs):
        context = super(WriteMessageMixin, self).get_context_data(**kwargs)
        self.write_message_tabs = [
            {'title': _('Doctor'),
             'href': reverse_lazy('patient:write_message_doctor'),
             },
            {'title': _('Support'),
             'href': reverse_lazy('patient:write_message_support'),
             },
        ]
        context['write_message_tabs'] = self.write_message_tabs
        context[
            'write_message_active_tab'] = self.get_active_write_message_tab()
        return context


class WriteDoctorMessageView(WriteMessageMixin, postman_views.WriteView):
    template_name = 'postman/write_to_doctor.html'
    write_message_active_tab = 1
    form_classes = (patient_forms.WriteMessageForm, AnonymousWriteForm)
    success_url = reverse_lazy('patient:sent')

    def get_form(self, form_class=None):
        form = super(WriteDoctorMessageView, self).get_form(form_class)
        patient = self.request.user.patient
        form.fields['case'].queryset = models.PatientCase.objects.filter(
            patient=patient)
        form.fields['recipients'].queryset = User.objects.filter(
            doctor__isnull=False,
            doctor__patientcase__patient=patient).distinct()

        return form


class SendNewMessage(WriteDoctorMessageView):
    template_name = 'postman/write_to_case_doctor.html'

    def get_form(self, form_class=None):
        form = super(SendNewMessage, self).get_form(form_class)
        case_id = self.kwargs.get('pk')
        case_queryset = models.PatientCase.objects.filter(id=case_id)
        case = case_queryset.get()
        doctor_user = case.doctor.user
        form.fields['case'].queryset = case_queryset
        form.fields['recipients'].queryset = User.objects.filter(
            pk=doctor_user.pk)
        form.fields['recipients'].initial = doctor_user
        form.fields['case'].initial = case
        return form

    def form_valid(self, form):
        message = form.save()
        return JsonResponse({
            'redirect': True,
            'success': True,
            'url': str(reverse_lazy('patient:case_messages',
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
            next_url = super(SendNewMessage, self).get_success_url()
        return next_url


class WriteSupportMessageView(WriteMessageMixin, postman_views.WriteView):
    template_name = 'postman/write_to_doctor.html'
    write_message_active_tab = 2
    form_classes = (patient_forms.WriteMessageSupportForm, AnonymousWriteForm)
    success_url = reverse_lazy('patient:sent')


class HelpSupport(PatientMixin, PatientMenuViewMixin,
                  generic.TemplateView):
    template_name = 'patient/dashboard/help_support.html'
    active_menu_ind = 4
    title = _('Help')


class MyAccountBaseView(PatientMixin, PatientMenuViewMixin,
                        utils_views.ActiveTabMixin):
    tabs = [
        {'img': 'img/my_account.png',
         'href': reverse_lazy('patient:my_account'),
         'header': _('Account Details'),
         },
        {'img': 'img/payment_info.png',
         'href': reverse_lazy('patient:payment'),
         'header': _('Payment Methods'),
         },
        {'img': 'img/billing.jpg',
         'href': reverse_lazy('patient:billing'),
         'header': _('Billing history'),
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


class DetailsView(MyAccountBaseView, generic.TemplateView):
    template_name = 'patient/account/details.html'
    active_tab_id = 1
    title = _('Account Details')
    success_message = _('Account details updated')

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user_form'] = utils_forms.DetailUserForm(instance=request.user)
        context['detail_form'] = patient_forms.DetailForm(
            instance=request.user.patient)
        return super(DetailsView, self).get(request, *args, **context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        user_form = utils_forms.DetailUserForm(request.POST,
                                               instance=request.user)
        detail_form = patient_forms.DetailForm(request.POST, request.FILES,
                                               instance=request.user.patient)
        if user_form.is_valid() and detail_form.is_valid():
            user_form.save()
            detail_form.save()
            messages.success(request, self.success_message)
            return HttpResponseRedirect(
                redirect_to=reverse_lazy('patient:my_account'))
        context['user_form'] = user_form
        context['detail_form'] = detail_form
        return render(request, self.template_name, context)


class PaymentView(MyAccountBaseView, generic.TemplateView):
    template_name = 'patient/account/payment.html'
    title = _('My Billing History')
    active_tab_id = 2

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        customer = self.request.user.customeruser.customer
        payment_methods = braintree.Customer.find(str(customer)).payment_methods
        if payment_methods:
            for method in payment_methods:
                if method.default:
                    method_representation = ''
                    method_type = type(method).__name__
                    if method_type == 'PayPalAccount':
                        method_representation = method_type + ' ' + method.email
                    elif method_type == 'CreditCard':
                        method_representation = method.card_type + ' ' + method.masked_number
                    context['payment_method'] = method_representation
        return context

    def get(self, request, *args, **kwargs):

        customer = request.user.customeruser.customer


        if request.is_ajax():
            case = request.GET.get('case')
            client_token = braintree.ClientToken.generate({
                "customer_id": customer
            })
            data = {
                'client_token': client_token}
            if case:
                doctor = models.Doctor.objects.get(patientcase__id=int(case))
                consult_rate = doctor.consult_rate
                deposit = doctor.deposit
                net_amount = consult_rate - deposit
                data['consult_rate'] = consult_rate
                data['deposit'] = deposit
                data['net_amount'] = net_amount
            return JsonResponse(data)
        return super(PaymentView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        nonce_from_the_client = request.POST.get('payment_method_nonce')
        customer = request.user.customeruser.customer
        result = braintree.PaymentMethod.create({
            "customer_id": customer,
            "payment_method_nonce": nonce_from_the_client,

        })
        if result.is_success:
            token = result.payment_method.token
            update_result = braintree.PaymentMethod.update(token, {
                "options": {
                  "make_default": True
                }

            })
        return HttpResponseRedirect(redirect_to=reverse_lazy('patient:payment'))


class BillingView(MyAccountBaseView, generic.TemplateView):
    template_name = 'patient/account/billing.html'
    title = _('My Billing History')
    active_tab_id = 3

    def get_context_data(self, **kwargs):
        context = super(BillingView, self).get_context_data()
        customer_id = self.request.user.customeruser.customer
        user_transactions = braintree.Transaction.search(
            braintree.TransactionSearch.customer_id == customer_id
        )
        context['transactions'] = user_transactions
        return context


class PasswordView(MyAccountBaseView, PasswordChangeTemplateMixin,
                   PasswordChangeView):
    success_url = reverse_lazy("patient:password")
    form_class = utils_forms.MyChangePassForm
    active_tab_id = 4
    title = _('Change Password')


class HistoryView(MyAccountBaseView, generic.TemplateView):
    template_name = 'patient/account/history.html'
    title = _('My Account')
    active_tab_id = 5

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['history_records'] = models.PatientHistory.objects.filter(
            patient=request.user.patient)
        return self.render_to_response(context)


class DoctorDetailView(PatientMixin, generic.DetailView):
    model = doctor_models.Doctor
    template_name = 'patient/dashboard/doctor_info.html'

    def get_context_data(self, **kwargs):
        context = super(DoctorDetailView, self).get_context_data(**kwargs)
        patient = self.request.user.patient
        query = doctor_models.DoctorAppointmentTime.objects.filter(
            doctor=self.object, start_time__gte=timezone.now(),
            free=True).exclude(
            Q(patientappointment__case__patient=self.request.user.patient) &
            Q(
                patientappointment__appointment_status=models.PatientAppointment.STATUS_EDIT))
        context['appointment_time'] = query
        return context


class PatientAppointmentProcess1View(PatientMixin, PatientActiveTabMixin,
                                     generic.View):
    def get(self, *args, **kwargs):
        patient = self.request.user.patient
        appointment_id = models.PatientAppointment.objects.filter(
            case__patient=patient,
            appointment_status=models.PatientAppointment.STATUS_EDIT).first().id

        if not patient.health_complete:
            self.process1[0]['finished'] = False

            next_url = reverse_lazy('patient:health_history_proc')
        elif not patient.lifestyle_complete:
            next_url = reverse_lazy('patient:lifestyle_proc')
        elif not patient.family_complete:
            next_url = reverse_lazy('patient:family_history_proc')
        else:
            next_url = reverse_lazy('patient:confirm')

        next_url += '?app_process=true'
        if appointment_id:
            next_url += '&pk=' + str(appointment_id)
        # if self.request.GET.get('case'):
        #     next_url += '&case=true'
        # return JsonResponse({'next_url': str(next_url)})
        return HttpResponseRedirect(next_url)


class PatientAppointmentProcessView(PatientMixin, PatientActiveTabMixin,
                                    generic.View):
    def get(self, *args, **kwargs):
        patient = self.request.user.patient
        pk = self.request.GET.get('pk')
        if not patient.health_complete:
            next_url = reverse_lazy('patient:my_health_history')
        elif not patient.lifestyle_complete:
            next_url = reverse_lazy('patient:my_lifestyle')
        elif not patient.family_complete:
            next_url = reverse_lazy('patient:my_family_history')
        else:
            next_url = reverse_lazy('patient:confirmation')

        next_url += '?app_process=true'
        if pk:
            next_url += '&pk=' + str(pk)
        # if self.request.GET.get('case'):
        #     next_url += '&case=true'
        # return JsonResponse({'next_url': str(next_url)})
        return HttpResponseRedirect(next_url)


class PatientHealthHistoryProcess(PatientMixin, PatientActiveTabMixin,
                                  generic.FormView):
    template_name = 'patient/dashboard/app_process/health_history.html'
    form_class = patient_forms.HealthHistoryForm
    active_proc1 = 1

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        try:
            health_history = models.PatientHealthHistory.objects.get(
                patient=self.request.user.patient)
            return form_class(instance=health_history, **self.get_form_kwargs())
        except models.PatientHealthHistory.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        form.save()
        self.request.user.patient.health_complete = True
        self.request.user.patient.save()
        return JsonResponse({'success': True,
                             'active_proc_num': self.get_active_proc1()[
                                 'number'],
                             'url': str(
                                 reverse_lazy('patient:appointment_process1'))})

    def form_invalid(self, form):
        data = {
            'success': False,
            'active_proc_num': self.get_active_proc1()['number'],
            'errors': form.errors
        }
        return JsonResponse(data)


# class SendNewMessage(generic.TemplateView):
class PatientLifestyleProcess(PatientMixin, PatientActiveTabMixin,
                              generic.FormView):
    template_name = 'patient/dashboard/app_process/lifestyle.html'
    form_class = patient_forms.LifestyleForm
    active_proc1 = 2

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        data = {'patient_id': self.request.user.patient.id,
                'height_ft': self.request.user.patient.height_ft,
                'height_in': self.request.user.patient.height_in,
                'weight': self.request.user.patient.weight}
        try:
            question_answers = models.PatientLifestyle.objects.filter(
                patient=self.request.user.patient)
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
                q_answer = models.PatientLifestyle.objects.get(
                    patient=self.request.user.patient, question=question)
            except models.PatientLifestyle.DoesNotExist:
                q_answer = models.PatientLifestyle(
                    patient=self.request.user.patient, question=question)
            q_answer.answer = form.cleaned_data['question_%s' % question.id]
            q_answer.save()
        self.request.user.patient.lifestyle_complete = True
        self.request.user.patient.save()
        return JsonResponse({'success': True,
                             'active_proc_num': self.get_active_proc1()[
                                 'number'],
                             'url': str(
                                 reverse_lazy('patient:appointment_process1'))})

    def form_invalid(self, form):
        data = {
            'success': False,
            'active_proc_num': self.get_active_proc1()['number'],
            'errors': form.errors
        }
        return JsonResponse(data)


class PatientFamilyHistoryProcess(PatientMixin, PatientActiveTabMixin,
                                  generic.FormView):
    template_name = 'patient/dashboard/app_process/family_history.html'
    form_class = patient_forms.FamilyHistoryForm
    active_proc1 = 3

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kw = self.get_form_kwargs()
        kw['initial'].update({'patient_id': self.request.user.patient.id})
        data = {}
        conditions = models.PatientFamilyCondition.objects.filter(
            Q(patient_id=self.request.user.patient.id) |
            Q(patient_id=None))
        for condition in conditions:
            try:
                data[
                    'condition_%s' % condition.id] = \
                    models.PatientFamily.objects.get(
                        condition=condition,
                        patient=self.request.user.patient).relationship_id
            except models.PatientFamily.DoesNotExist:
                pass
        kw['initial'].update(data)
        return form_class(**kw)

    def form_valid(self, form):
        conditions = models.PatientFamilyCondition.objects.filter(
            Q(patient_id=self.request.user.patient.id) |
            Q(patient_id=None))
        for condition in conditions:
            if form.cleaned_data['condition_%s' % condition.id]:
                try:
                    relation = models.PatientFamily.objects.get(
                        condition=condition, patient=self.request.user.patient)
                except models.PatientFamily.DoesNotExist:
                    relation = models.PatientFamily(
                        condition=condition,
                        patient=self.request.user.patient)
                relation.relationship = form.cleaned_data[
                    'condition_%s' % condition.id]
                relation.save()
        self.request.user.patient.family_complete = True
        self.request.user.patient.save()
        return JsonResponse({'success': True,
                             'active_proc_num': self.get_active_proc1()[
                                 'number'],
                             'url': str(
                                 reverse_lazy('patient:appointment_process1'))})

    def form_invalid(self, form):
        data = {
            'success': False,
            'active_proc_num': self.get_active_proc1()['number'],
            'errors': form.errors
        }
        return JsonResponse(data)


class ConfirmProcessView(PatientMenuViewMixin, PatientActiveTabMixin,
                         generic.TemplateView, PatientMixin):
    template_name = 'patient/dashboard/app_process/confirm.html'
    active_menu_ind = 1
    title = _('Confirmation')
    active_proc1 = 4
    success_message = _('Your payment has been successfully processed')
    failure_message = _('Something went wrong. Please check your payment info')

    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmProcessView, self).get_context_data(
            *args,
            **kwargs)
        context['patient'] = self.request.user.patient
        pk = self.request.GET.get('pk')
        data = doctor_views.get_appointment_data(int(pk), context)
        context['taken'] = False
        context.update(data)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        appointment = models.PatientAppointment.objects.get(
            pk=context['appointment_id'])
        if appointment.appointment_time.free:
            appointment.appointment_time.free = False
            appointment.appointment_status = \
                models.PatientAppointment.STATUS_NEW
            appointment.appointment_time.save()
            appointment.save()
            context['error'] = False
            context['taken'] = True

            case = models.PatientCase.objects.get(
                patientappointment=appointment)
            doctor = doctor_models.Doctor.objects.get(patientcase=case)
            customer_id = self.request.user.customeruser.customer
            nonce_from_the_client = self.request.POST.get('payment_method_nonce')

            result = braintree.Transaction.sale({
                "customer_id": str(customer_id),
                "amount": str(doctor.deposit),
                "merchant_account_id": settings.MERCHANT_ID,
                "payment_method_nonce": nonce_from_the_client,
                "custom_fields": {
                    "type": "Deposit",
                    "appointment_date": appointment.appointment_time.start_time,
                    "case": case.problem
                },

                "options": {
                    "submit_for_settlement": True,
                }
            })

            next_title = _('Appointment Created')
            next_button = _('Continue')

            if result.is_success:
                appointment.deposit_paid = True
                appointment.deposit_transaction = result.transaction.id
                appointment.save()
                next_text = str(_(
                    'The appointment has been created and you are being '
                    'redirected to the associated case so that you can '
                    'upload any files associated with the issue. ')) + \
                            str(self.success_message)
                next_url = reverse_lazy('patient:case_appointment',
                                        kwargs={'pk': appointment.case_id})
            else:
                next_text = self.failure_message
                next_url = str(reverse_lazy('patient:payment')) + '?next_url=' + \
                           str(reverse_lazy('patient:case_appointment',
                                            kwargs={'pk': appointment.case_id}))

            return JsonResponse({
                'success': True,
                'active_proc_num': self.get_active_proc1()['number'],
                'next_title': str(next_title),
                'next_text': str(next_text),
                'next_button': str(next_button),
                'url': str(next_url)
            })
        else:
            context['error'] = True
            context['taken'] = True
            return JsonResponse({
                'success': False,
                'active_proc_num': self.get_active_proc1()['number'],
            })


class PatientAppointmentView(PatientMixin, generic.FormView):
    template_name = 'patient/appointment_request.html'
    form_class = patient_forms.PatientAppointmentForm
    success_url = reverse_lazy('patient:appointment_process')
    success_message = _('Your payment has been successfully processed')
    failure_message = _('Something went wrong. Please check your payment info')

    def get_initial(self):
        initial = super(PatientAppointmentView, self).get_initial()
        patient = self.request.user.patient
        initial['patient'] = patient
        time = models.DoctorAppointmentTime.objects.get(
            pk=self.kwargs.get('pk'))
        initial['appointment_time'] = time
        initial['doctor'] = time.doctor
        initial[
            'appointment_type'] = models.PatientAppointment.VIDEO_APPOINTMENT
        return initial

    def get_context_data(self, **kwargs):
        context = super(PatientAppointmentView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['deposit'] = models.Doctor.objects.get(
            doctorappointmenttime__id=pk).deposit
        return context

    def get_form(self, form_class=None):
        form = super(PatientAppointmentView, self).get_form(form_class)
        patient = self.request.user.patient
        form.fields['patient'].queryset = models.Patient.objects.filter(
            id=patient.id)
        time = models.DoctorAppointmentTime.objects.get(
            pk=self.kwargs.get('pk'))
        form.fields['doctor'].queryset = doctor_models.Doctor.objects.filter(
            id=time.doctor.id)
        form.fields['case'].queryset = models.PatientCase.objects.filter(
            patient=patient, doctor=time.doctor)
        choices = []
        # if time.doctor.phone_appointment:
        #     choices.append(models.PatientAppointment.APPOINTMENT_CHOICES[0])
        # if time.doctor.video_appointment:
        choices.append(models.PatientAppointment.APPOINTMENT_CHOICES[1])
        # if not choices:
        #     choices.append(('', _('Not available')))
        form.fields['appointment_type'].choices = choices
        return form

    def form_valid(self, form):
        is_follow_up = form.cleaned_data['follow_up']
        appointment = form.save()
        patient = self.request.user.patient
        if patient.family_complete and patient.health_complete and patient.lifestyle_complete:
            appointment.appointment_status = models.PatientAppointment.STATUS_NEW
            appointment.appointment_time.free = False
            appointment.appointment_time.save()
            appointment.save()
            case = models.PatientCase.objects.get(
                patientappointment=appointment)
            doctor = doctor_models.Doctor.objects.get(patientcase=case)
            customer_id = self.request.user.customeruser.customer
            nonce_from_the_client = self.request.POST.get('payment_method_nonce')
            result = braintree.Transaction.sale({
                "customer_id": str(customer_id),
                "amount": str(doctor.deposit),
                "merchant_account_id": settings.MERCHANT_ID,
                "payment_method_nonce": nonce_from_the_client,
                "custom_fields": {
                    "type": "Deposit",
                    "appointment_date": appointment.appointment_time.start_time,
                    "case": case.problem
                },

                "options": {
                    "submit_for_settlement": True,

                }
            })
            next_title = _('Appointment Created')
            if result.is_success:
                appointment.deposit_paid = True
                appointment.deposit_transaction = result.transaction.id
                appointment.save()
                if is_follow_up:
                    next_text = str(_('The appointment has been successfully '
                                      'created. ')) + str(self.success_message)
                    next_url = ''
                    next_button = _('OK')
                else:

                    next_text = str(_(
                        'The appointment has been created and you are being '
                        'redirected to the associated case so that you can '
                        'upload any files associated with the issue. ')) + \
                                str(self.success_message)
                    next_url = reverse_lazy('patient:case_appointment',
                                            kwargs={'pk': appointment.case_id})
                    next_button = _('Continue')

            else:
                next_text = self.failure_message
                next_url = str(reverse_lazy('patient:payment')) + '?next_url=' + \
                           str(reverse_lazy('patient:case_appointment',
                                            kwargs={'pk': appointment.case_id}))
                next_button = _('Continue')

        else:
            next_title = _('Incomplete Profile')
            next_text = _('In order to confirm an appointment, you need to '
                          'complete your health history and/or '
                          'payment information')
            next_url = '#proccessModal'
            next_button = _('Continue')

        add_file_url = reverse_lazy('patient:case_files',
                                    kwargs={'pk': appointment.case_id})
        case_url = reverse_lazy('patient:appointment_process')
        add_file_url += '?app_process=true&case=true' + '&pk=' + str(
            appointment.id)
        case_url += '?pk=' + str(appointment.id)
        cancel_url = str(reverse_lazy('patient:consultation_status', kwargs={
            'id_appointment': appointment.id,
            'status': models.PatientAppointment.STATUS_PATIENT_CANCEL}))
        return JsonResponse({'success': True,
                             'url': self.get_success_url(),
                             'case_url': str(case_url),
                             'add_file': str(add_file_url),
                             'id': str(appointment.id),
                             'cancel_url': cancel_url,
                             'next_text': str(next_text),
                             'next_url': str(next_url),
                             'next_title': str(next_title),
                             'next_button': str(next_button)
                             })

    def form_invalid(self, form):
        data = {
            'success': False,
            'errors': form.errors
        }
        if '__all__' in form.errors.iterkeys():
            case_id = models.PatientAppointment.objects.filter(
                appointment_status=models.PatientAppointment.STATUS_EDIT,
                case__patient=self.request.user.patient). \
                first().case.id
            data['case_url'] = str(reverse_lazy('patient:case_appointment',
                                                kwargs={'pk': case_id}))
        return JsonResponse(data)


class ConfirmAppointmentProcessView(PatientMenuViewMixin, PatientActiveTabMixin,
                                    generic.TemplateView, PatientMixin):
    template_name = 'patient/confirmation.html'
    active_menu_ind = 1
    title = _('Confirmation')
    active_proc = 4
    active_proc1 = 4
    success_message = _('New appointment created. '
                        'Your payment has been successfully processed')
    failure_message = _('Something went wrong. Please check your payment info')

    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmAppointmentProcessView, self).get_context_data(
            *args,
            **kwargs)
        context['patient'] = self.request.user.patient
        context['old_process'] = True
        pk = self.request.GET.get('pk')
        data = doctor_views.get_appointment_data(int(pk), context)
        context['taken'] = False
        context.update(data)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        appointment = models.PatientAppointment.objects.get(
            pk=context['appointment_id'])
        if appointment.appointment_time.free:
            appointment.appointment_time.free = False
            appointment.appointment_status = \
                models.PatientAppointment.STATUS_NEW
            appointment.appointment_time.save()
            appointment.save()
            context['error'] = False
            context['taken'] = True
            case = models.PatientCase.objects.get(
                patientappointment=appointment)
            doctor = doctor_models.Doctor.objects.get(patientcase=case)
            customer_id = self.request.user.customeruser.customer
            nonce_from_the_client = self.request.POST.get('payment_method_nonce')
            result = braintree.Transaction.sale({
                "customer_id": str(customer_id),
                "amount": str(doctor.deposit),
                "merchant_account_id": settings.MERCHANT_ID,
                "payment_method_nonce": nonce_from_the_client,
                "custom_fields": {
                    "type": "Deposit",
                    "appointment_date": appointment.appointment_time.start_time,
                    "case": case.problem
                },

                "options": {
                    "submit_for_settlement": True,
                }
            })

            if result.is_success:
                appointment.deposit_paid = True
                appointment.deposit_transaction = result.transaction.id
                appointment.save()
                messages.success(request, self.success_message)
            else:
                messages.error(request, self.failure_message)


        else:
            context['error'] = True
            context['taken'] = True
        return HttpResponseRedirect(reverse_lazy(
            'patient:case_appointment', kwargs={'pk': appointment.case_id}))


class ConsultationView(PatientMixin, PatientMenuViewMixin,
                       PatientActiveTabMixin, generic.TemplateView):
    active_menu_ind = 2
    template_name = 'patient/dashboard/my_health/consultation.html'
    title = _('Consultation History')
    success_message = _('Consultation updated')
    active_tab_id = 2
    base_active_tab = 2

    def get(self, request, id_appointment=None, status=None, *args, **kwargs):
        context = self.get_context_data()
        if status:
            status = int(status)
            if id_appointment:
                try:
                    appointment = models.PatientAppointment.objects.get(
                        pk=id_appointment)
                except models.PatientAppointment.DoesNotExist:
                    return Http404(**context)
                case_pk = request.GET.get('pk')
                if not case_pk:
                    case_pk = appointment.case.id

                if appointment.appointment_status == \
                        models.PatientAppointment.STATUS_EDIT and \
                                status == models.PatientAppointment.STATUS_PATIENT_CANCEL:
                    case = appointment.case
                    appointment.delete()

                    if not case.patientappointment_set.exists():
                        case.delete()
                    if request.is_ajax():
                        return HttpResponse()
                    else:
                        url = reverse_lazy('patient:all_cases',
                                           kwargs={'type': 'open'})
                        return HttpResponseRedirect(redirect_to=url)

                else:
                    appointment.appointment_status = status
                    if status == models.PatientAppointment.STATUS_DOCTOR_CANCEL or \
                                    status == models.PatientAppointment.STATUS_PATIENT_CANCEL:
                        appointment.appointment_time.free = True
                        appointment.appointment_time.save()
                    appointment.save()
                url = self.request.GET.get('next')
                if not url:
                    url = reverse_lazy('patient:case_appointment',
                                       kwargs={'pk': case_pk})
                return HttpResponseRedirect(redirect_to=url)
            else:
                return Http404(**context)
        context['appointments'] = models.PatientAppointment.objects.filter(
            case__patient=request.user.patient,
            appointment_time__start_time__gte=timezone.now().date()) \
            .order_by('appointment_time')

        return super(ConsultationView, self).get(request, *args, **context)


class ConsultationEdit(PatientMixin, PatientMenuViewMixin,
                       PatientActiveTabMixin, generic.FormView):
    active_menu_ind = 2
    template_name = 'patient/dashboard/my_health/consultation_edit.html'
    form_class = patient_forms.PatientConsultationForm
    base_active_tab = 4

    def get_form_kwargs(self):
        kwargs = super(ConsultationEdit, self).get_form_kwargs()
        instance = models.PatientAppointment.objects.get(
            pk=self.kwargs.get('pk'))
        kwargs.update({'instance': instance})
        return kwargs

    def form_valid(self, form):
        instance = form.save()
        self.instance = instance
        return super(ConsultationEdit, self).form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            case_pk = self.instance.case.pk
            next_url = reverse_lazy('patient:case_appointment',
                                    kwargs={'pk': case_pk})
        return next_url


def get_all_doctors_json(request):
    query = doctor_models.Doctor.objects.exclude(user__first_name='',
                                                 user__last_name='')
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
    data = {'': _('Select')}
    if pk:
        query = doctor_models.DoctorAppointmentDate.objects.get(
            pk=pk).doctorappointmenttime_set.filter(free=True)
        if query:
            for date in query:
                data.update({date.pk: date.name})
        else:
            data = {'': _("Don't have time")}
    return JsonResponse(data)


def get_all_cases_json(request):
    pk = request.GET.get('pk')
    patient = request.user.patient
    data = {}
    query = models.PatientCase.objects.filter(doctor__user__id=pk,
                                              patient=patient)
    if query:
        for item in query:
            data.update({item.pk: item.problem[:40]})
    # data.update({'': str(_('Select'))})
    return JsonResponse(data)


class CaseActiveTabMixin(PatientMenuViewMixin, PatientActiveTabMixin):
    tabs = [
        {'title': _('Open'),
         'href': reverse_lazy('patient:all_cases', kwargs={'type': 'open'})},
        {'title': _('Closed'),
         'href': reverse_lazy('patient:all_cases', kwargs={'type': 'close'})},
    ]
    active_proc = 1


class PatientCaseListView(PatientMixin,
                          CaseActiveTabMixin, PatientActiveTabMixin,
                          generic.ListView):
    template_name = 'patient/case/case_list.html'
    active_menu_ind = 2
    active_tab_id = 1
    base_active_tab = 4
    title = _('Open case')
    type = 'open'
    success_url = reverse_lazy('patient:all_cases', kwargs={'type': type})
    paginate_by = 10

    def get_queryset(self):
        queryset = models.PatientCase.objects.filter(
            patient=self.request.user.patient)
        if self.type == 'open':
            queryset = queryset.filter(status=models.PatientCase.OPEN)
        else:
            queryset = queryset.filter(status=models.PatientCase.CLOSED)
        doctor = self.request.GET.get('doctor')
        search_query = self.request.GET.get('search')
        if doctor:
            queryset = queryset.filter(doctor__id=doctor)
        if search_query:
            queryset = queryset.filter(Q(problem__icontains=search_query) |
                                       Q(description__icontains=search_query))
        queryset.distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PatientCaseListView, self).get_context_data(**kwargs)
        context['type'] = self.type
        doctors = doctor_models.Doctor.objects.filter(
            patientcase__patient=self.request.user.patient).distinct()
        context['doctors'] = doctors
        return context

    def get(self, request, type=None, *args, **kwargs):
        self.type = type
        if type == 'close':
            self.active_tab_id = 2
        return super(PatientCaseListView, self).get(request, *args, **kwargs)


class PatientCaseMixin(PatientMixin, CaseActiveTabMixin, PatientActiveTabMixin):
    case_tabs = []
    case_tab_id = 0
    active_menu_ind = 2
    title = _('Cases')
    base_active_tab = 4

    def get_active_case_tab(self):
        return self.case_tabs[self.case_tab_id - 1]

    def get_context_data(self, **kwargs):
        context = super(PatientCaseMixin, self).get_context_data(**kwargs)
        self.case_tabs = [
            {'title': _('Case Overview'),
             'href': reverse_lazy('patient:case_overview',
                                  kwargs={'pk': self.kwargs.get('pk')})},
            {'title': _('Appointments'),
             'href': reverse_lazy('patient:case_appointment',
                                  kwargs={'pk': self.kwargs.get('pk')})},
            {'title': _('Files / Tests'),
             'href': reverse_lazy('patient:case_files',
                                  kwargs={'pk': self.kwargs.get('pk')})},
            {'title': _('Doctor Notes'),
             'href': reverse_lazy('patient:doctor_notes',
                                  kwargs={'pk': self.kwargs.get('pk')})},

            {'title': _('Messages'),
             'href': reverse_lazy('patient:case_messages',
                                  kwargs={'pk': self.kwargs.get('pk')})},
        ]
        context['case_tabs'] = self.case_tabs
        pk = self.kwargs.get('pk')
        if pk:
            try:
                case = models.PatientCase.objects.get(
                    pk=pk, patient=self.request.user.patient)
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


class PatientCaseDetailView(PatientCaseMixin, generic.DetailView):
    model = models.PatientCase
    template_name = 'patient/case/overview.html'
    context_object_name = 'case'
    case_tab_id = 1

    def get_object(self, queryset=None):
        try:
            obj = super(PatientCaseDetailView, self).get_object(queryset)
        except Http404:
            obj = None
        return obj


class PatientCaseAppointmentView(PatientCaseMixin, generic.ListView):
    model = models.PatientAppointment
    template_name = 'patient/case/appointments.html'
    context_object_name = 'appointments'
    case_tab_id = 2

    def get_queryset(self):
        case_id = self.kwargs.get('pk')
        return models.PatientAppointment.objects.filter(case_id=case_id)

    def get_context_data(self, **kwargs):
        context = super(PatientCaseAppointmentView, self).get_context_data(
            **kwargs)
        context['appointment_availability'] = get_appointment_room_availability(self.object_list)
        return context


class AppointmentDepositPayment(PatientCaseMixin, generic.View):
    case_tab_id = 2
    success_message = _('Your payment has been successfully processed')
    failure_message = _('Something went wrong. Please check your payment info')

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        appointment = kwargs.get('appointment')
        doctor = doctor_models.Doctor.objects.get(patientcase__id=pk)
        appointment_obj = models.PatientAppointment.objects.get(id=appointment)
        case = models.PatientCase.objects.get(id=pk)
        customer_id = self.request.user.customeruser.customer
        nonce_from_the_client = self.request.GET.get('payment_method_nonce')

        result = braintree.Transaction.sale({
            "customer_id": str(customer_id),
            "amount": str(doctor.deposit),
            "merchant_account_id": settings.MERCHANT_ID,
            "payment_method_nonce": nonce_from_the_client,
            "custom_fields": {
                "type": "Deposit",
                "appointment_date": appointment_obj.appointment_time.start_time,
                "case": case.problem
            },

            "options": {
                "submit_for_settlement": True,
            }
        })
        if result.is_success:
            messages.success(self.request, self.success_message)
            appointment = models.PatientAppointment.objects.get(pk=appointment)
            appointment.deposit_paid = True
            appointment.deposit_transaction = result.transaction.id
            appointment.save()
            redirect_url = reverse_lazy('patient:case_appointment',
                                        kwargs={'pk': pk})
        else:
            messages.error(self.request, self.failure_message)
            redirect_url = reverse_lazy('patient:payment')
            redirect_url += '?next_url=' + str(
                reverse_lazy('patient:case_appointment', kwargs={'pk': pk}))

        return HttpResponseRedirect(redirect_url)


class AppointmentRatePayment(generic.View):
    success_message = _('The appointment has been completed. '
                        'Consult rate has been successfully taken')
    failure_message = _('Something went wrong. Check your payment info')

    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('appointment')
        appointment = models.PatientAppointment.objects.get(id=appointment_id)
        transaction_id = appointment.consult_transaction
        result = braintree.Transaction.submit_for_settlement(transaction_id)
        if result.is_success:
            appointment.appointment_status = models.PatientAppointment.STATUS_COMPLETE
            appointment.save()
            messages.success(request, self.success_message)
            redirect_url = reverse_lazy('patient:dashboard')
        else:
            messages.error(request, self.failure_message)
            redirect_url = str(reverse_lazy('patient:payment')) + '?next_url=' \
                           + str(reverse_lazy('patient:after_appointment',
                                              kwargs={'pk': kwargs.get('pk'),
                                                      'appointment': appointment_id}))

        return HttpResponseRedirect(redirect_url)


class PatientCaseNoteView(PatientCaseMixin, generic.ListView):
    model = models.PatientAppointment
    template_name = 'patient/case/notes.html'
    context_object_name = 'appointments'
    case_tab_id = 4

    def get_queryset(self):
        case_id = self.kwargs.get('pk')
        query = models.PatientAppointment.objects.filter(case_id=case_id)
        return query.filter(appointmentnote__public_notes__isnull=False)


class PatientCaseFilesView(PatientCaseMixin, generic.ListView):
    model = models.TestFileRecord
    template_name = 'patient/case/case_files.html'
    context_object_name = 'files'
    case_tab_id = 3

    def get_queryset(self):
        case_id = self.kwargs.get('pk')
        return models.TestFileRecord.objects.filter(case__id=case_id)

    def get_context_data(self, **kwargs):
        context = super(PatientCaseFilesView, self).get_context_data(**kwargs)
        context['case_id'] = self.kwargs.get('pk')
        return context


class PatientCaseMessagesView(PatientCaseMixin, postman_views.FolderMixin,
                              generic.TemplateView):
    template_name = 'postman/case_messages.html'
    case_tab_id = 5
    folder_name = 'sent'
    view_name = 'sent'

    def get_context_data(self, **kwargs):
        context = super(PatientCaseMessagesView, self).get_context_data(
            **kwargs)
        case_id = self.kwargs.get('pk')
        filters = [Q(casemessage__case_id=case_id) | Q(
            thread__casemessage__case_id=case_id)]
        inbox = Message.objects.inbox(self.request.user, True).filter(*filters,
                                                                      thread__isnull=True)
        sent = Message.objects.sent(self.request.user).filter(*filters)
        pm_messages = sorted(chain(inbox, sent),
                             key=lambda x: x.sent_at, reverse=True)
        context['pm_messages'] = pm_messages
        return context


class PatientCaseAddFileView(PatientCaseMixin, generic.CreateView):
    model = models.TestFileRecord
    template_name = 'patient/case/upload_files.html'
    form_class = patient_forms.FilesAddForm
    case_tab_id = 3

    def get_context_data(self, **kwargs):
        context = super(PatientCaseAddFileView, self).get_context_data(**kwargs)

        if not context.get('additionalfiles_formset'):
            context['additionalfiles_formset'] = \
                patient_forms.AdditionalFilesInlineFormSet(
                    instance=models.TestFileRecord())
        return context

    def get_form(self, form_class=None):
        form = super(PatientCaseAddFileView, self).get_form(form_class)
        case_id = self.kwargs.get('pk')
        form.fields['case'].queryset = models.PatientCase.objects.filter(
            id=case_id)
        form.fields['case'].initial = models.PatientCase.objects.filter(
            id=case_id)
        return form

    def form_valid(self, form, formset):
        self.object = formset.instance = form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        self.object = None
        return self.render_to_response(
            self.get_context_data(
                form=form,
                additionalfiles_formset=formset,
            )
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        additionalfiles_formset = patient_forms.AdditionalFilesInlineFormSet(
            request.POST, request.FILES)

        if form.is_valid() and additionalfiles_formset.is_valid():
            return self.form_valid(form, additionalfiles_formset)
        else:
            return self.form_invalid(form, additionalfiles_formset)

    def get_success_url(self):
        next_url = reverse_lazy('patient:case_files',
                                kwargs={'pk': self.kwargs.get('pk')})
        pk = self.request.GET.get('pk', None)
        if next_url:
            if pk:
                if self.request.GET.get('case'):
                    next_url += '?app_process=true&case=true'
                return str(next_url + '&pk=' + pk)
            return next_url
        else:
            if pk:

                if self.request.GET.get('case'):
                    next_url += '?app_process=true&case=true'
                return str(self.success_url + '&pk=' + pk)
            return self.success_url


class PatientTestFileRecordDeleteView(PatientCaseMixin, generic.DeleteView):
    model = models.TestFileRecord

    def get_success_url(self):
        next_url = reverse_lazy('patient:case_files',
                                kwargs={'pk': self.kwargs.get('case')})
        pk = self.request.GET.get('pk', None)
        if pk:
            if self.request.GET.get('case'):
                next_url += '?app_process=true&case=true'
            return str(next_url + '&pk=' + pk)
        return next_url

