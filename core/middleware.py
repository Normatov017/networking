from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

EXCLUDED_URLS = [
    '/login/',
    '/admin/',       # Admin paneliga kirish uchun
    '/logout/',
    '/signup/',      # Ro'yxatdan o'tish bo'lsa
    # kerakli boshqa URL'lar bo'lsa, qo‘shing
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Agar so‘rov URLlar ro‘yxatida bo‘lsa, tekshirishsiz davom etadi
        if request.path in EXCLUDED_URLS or request.user.is_authenticated:
            return self.get_response(request)

        return redirect('/login/')