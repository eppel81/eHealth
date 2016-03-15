from django.conf.urls import include, url, static
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm, \
    password_reset_done, password_reset, password_reset_complete
from patient import urls as patient_urls
from doctor import urls as doctor_urls
from utils import urls as util_urls
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from utils import forms


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(

    url(r'^doctor/', include(doctor_urls, namespace='doctor')),
    url(r'^accounts/password/reset/$', password_reset,
        {'post_reset_redirect': '/accounts/password/reset/done/',
         'template_name': 'account/password_reset_form.html',
         'email_template_name': 'account/password_reset_email.html',
         'password_reset_form': forms.MyResetPassForm},
        name='account_reset_password'
        ),
    url(r'^accounts/password/reset/done/$', password_reset_done,
        {'template_name': 'account/password_reset_done.html'}
        ),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm,
        {'post_reset_redirect': '/accounts/password/done/',
         'template_name': 'account/password_reset_confirm.html',
         'set_password_form': forms.MySetPassForm},
        name='password_reset_confirm'
        ),

    url(r'^accounts/password/done/$', password_reset_complete,
         {'template_name': 'account/password_reset_complete.html'}
        ),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'^braintree/', include('django_braintree.urls')),
    url(r'^', include(patient_urls, namespace='patient')),
    url(r'^', include(util_urls, namespace='utils')),
)