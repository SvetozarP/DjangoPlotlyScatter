from django.urls import path

from core import views

urlpatterns = [
    path('', views.plot, name='scatter'),
]