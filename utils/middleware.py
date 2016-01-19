import pytz
from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        person = None
        if request.user.is_authenticated():
            person = request.user.doctor_set.first()
            if not person:
                person = request.user.patient_set.first()
        if person:
            tzname = person.timezone.name
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
