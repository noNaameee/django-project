from django.urls import path,include
from app.views import Register
from django.contrib.auth import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('register/',Register.as_view(),name='register'),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#python manage.py runserver