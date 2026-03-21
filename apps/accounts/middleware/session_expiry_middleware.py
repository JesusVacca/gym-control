from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect

class SessionExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            login_time = request.session.get('login_time')
            if login_time:
                elapsed = timezone.now().timestamp() - login_time
                if elapsed > (6 * 60 * 60):
                    logout(request)
                    return redirect('accounts:login')
        return self.get_response(request)