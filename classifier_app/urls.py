# classifier_app/urls.py

from django.urls import path
from . import views # Make sure 'views' is correctly imported from current directory

urlpatterns = [
    path('', views.symptom_classifier_view, name='symptom_classifier'),
]