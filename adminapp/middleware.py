from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import logout

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                # Convert ISO string to datetime object
                last_activity_time = timezone.datetime.fromisoformat(last_activity)

                # Ensure timezone-awareness
                if timezone.is_naive(last_activity_time):
                    last_activity_time = timezone.make_aware(last_activity_time)

                # Check if inactive for 2+ hours
                if now - last_activity_time > timedelta(hours=2):
                    logout(request)
            # Update last activity
            request.session['last_activity'] = now.isoformat()

        return self.get_response(request)
