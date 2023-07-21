# image_app/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('upload/', views.upload, name='upload'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
