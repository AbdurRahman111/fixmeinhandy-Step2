from django.urls import path 
from . import views

# URLConf module
urlpatterns = [
    path('download_sendung', views.api_to_pdf, name="download_sendung"),
]   