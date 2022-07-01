from django.urls import path

from example.health.api import views
from example.health.apps import HealthConfig

app_name = HealthConfig.name

urlpatterns = [
    path('', views.HealthView.as_view(), name='health'),
]
