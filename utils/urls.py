from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^terms/$', views.home, name='terms_conditions'),
    url(r'^about/$', views.about, name='about_us'),
]
