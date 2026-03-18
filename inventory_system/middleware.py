from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than the login/logout pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            path = request.path_info
            
            # Exempt routes
            if not (path.startswith(settings.LOGIN_URL) or \
                    path.startswith('/accounts/') or \
                    path.startswith('/admin/') or \
                    path.startswith('/static/')):
                # Redirect to login page and keep the 'next' parameter
                return redirect(f"{settings.LOGIN_URL}?next={path}")
                
        response = self.get_response(request)
        return response
