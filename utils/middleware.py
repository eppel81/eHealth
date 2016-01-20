from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        person = None
        current_timezone = 'Etc/UTC'
        if request.user.is_authenticated():
            if hasattr(request.user, 'doctor'):
                person = request.user.doctor
            else:
                person = request.user.patient
            if person.timezone is not None:
                current_timezone = person.timezone.name
        timezone.activate(current_timezone)

