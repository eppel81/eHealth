from django.utils import timezone


class TimezoneMiddleware(object):
    default_tz = 'Etc/UTC'

    def process_request(self, request):
        current_timezone = self.default_tz
        if request.user.is_authenticated():
            person = getattr(request.user, 'doctor', None)
            if not person:
                person = getattr(request.user, 'patient', None)
            if not person:
                person = getattr(request.user, 'supportuser', None)
            if person and person.timezone is not None:
                current_timezone = person.timezone.name
        timezone.activate(current_timezone)

