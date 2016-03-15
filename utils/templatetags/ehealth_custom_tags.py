import string
from datetime import datetime
from django import template
from django.template.defaultfilters import stringfilter
from django.utils import timezone
import pytz

register = template.Library()


@register.filter
@stringfilter
def endswith(value, param):
    return value.endswith(param)


@register.filter(is_safe=False)
def default_if_exists(value, arg):
    if value is not False and not value:
        return arg
    return value


@register.filter()
def get_available_time(doctor, patient):
    return doctor.get_available_time(patient)


@register.filter()
@stringfilter
def convert_title(initial_title):
    return string.capwords(initial_title, '_').replace('_', ' ')


@register.filter()
def str_to_date(date_string):
    if date_string:
        date_pattern = "%Y-%m-%d %H:%M:%S %Z"
        date_time = datetime.strptime(date_string, date_pattern).replace(
            tzinfo=pytz.timezone('UTC'))
        return date_time
    else:
        return ''


@register.assignment_tag()
def get_url_attrs(*args, **kwargs):
    attributes = str()
    for key, value in kwargs.iteritems():
        if value:
            attributes += '&' + key + '=' + value
    return attributes
