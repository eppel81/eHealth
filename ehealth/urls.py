from django.conf.urls import include, url, static
from django.contrib import admin
from patient import urls as patient_urls
from doctor import urls as doctor_urls
from utils import urls as util_urls
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^doctor/', include(doctor_urls, namespace='doctor')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^', include(patient_urls, namespace='patient')),
    url(r'^', include(util_urls, namespace='utils')),
)