from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.contact_submission, name='contact-submission'),
]