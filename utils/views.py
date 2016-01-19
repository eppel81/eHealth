from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class MenuViewMixin(object):
    options = []
    title = ''
    active_menu_ind = 0
    success_message = None
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

    def form_valid(self, form):
        res = super(MenuViewMixin, self).form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return res


class ActiveTabMixin(object):
    tabs = []
    process = []
    active_tab_id = 0
    active_proc = 0

    def get_active_tab(self):
        return self.tabs[self.active_tab_id-1]

    def get_active_proc(self):
        for item in self.process:
            if item['number'] <= self.active_proc:
                item['finished'] = True
        return self.process[self.active_proc-1]

    def get_context_data(self, **kwargs):
        data = super(ActiveTabMixin, self).get_context_data(**kwargs)
        data['tabs'] = self.tabs
        data['active_tab'] = self.get_active_tab()
        data['process'] = self.process
        if self.process:
            data['active_proc'] = self.get_active_proc()
        return data


def home(request):
    if request.user.is_authenticated():
        if request.session['type_user'] == 'patient':
            return HttpResponseRedirect(redirect_to=reverse('patient:dashboard'))
        elif request.session['type_user'] == 'doctor':
            return HttpResponseRedirect(redirect_to=reverse('doctor:dashboard'))
    else:
        list(messages.get_messages(request))
    return render(request, 'home.html')


def terms(request):
    return render(request, 'terms.html')


def about(request):
    return render(request, 'about.html')


class LoginRequiredViewMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredViewMixin, self).dispatch(*args, **kwargs)


class PasswordChangeTemplateMixin(object):

    def get_context_data(self, **kwargs):
        data = super(PasswordChangeTemplateMixin, self).get_context_data(**kwargs)
        data['user_type_template'] = self.request.session['type_user']+'/account/base_account.html'
        data['form_action_url'] = self.request.session['type_user']+':password'
        return data
