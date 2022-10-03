from django.urls import path
from ussd_app import views

urlpatterns = [
    path('demo', views.ussd_callback, name=('demo'))
]
