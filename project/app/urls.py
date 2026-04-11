from django.urls import path,include
from app.views import Register
from django.contrib.auth import views
urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('register/',Register.as_view(),name='register'),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
]