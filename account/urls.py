from django.urls import path
from . import views

# URLConf module
urlpatterns = [
    path('my_profile/', views.my_profile, name="my_profile"),
    path('login_func/', views.login_func, name="login_func"),
    path('registration/', views.registration, name="registration"),
    path('logout_func/', views.logout_func, name="logout_func"),
]