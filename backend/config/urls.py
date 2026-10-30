from django.http import JsonResponse
from django.urls import path, include


def home(request):
    return JsonResponse({
        "message": "Coffee Shop API is running",
        "status": "success"
    })


urlpatterns = [
    path('', home, name='home'),
    path('api/', include('catalog.urls')),
]
