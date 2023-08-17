from django.urls import path 
from . import views

# URLConf module
urlpatterns = [
    path('', views.schadensrechnung, name="schadensrechnung"),
    path('get_handy_namen/', views.get_handy_namen),
    path('get_schadensart/', views.get_schadensart),
    path('get_preis/', views.get_preis),
    path('Impressum/', views.Impressum, name='Impressum'),
    path('Datenschutzerklarung/', views.Datenschutzerklarung, name="Datenschutzerklarung"),
]   