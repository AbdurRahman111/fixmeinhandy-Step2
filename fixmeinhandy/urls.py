"""
URL configuration for fixmeinhandy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from benutzer import views as benutzer_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('allgemeine_daten/', benutzer_views.kundendaten, name='dateneingabe'), #dateneingabe
    path('my_order/', benutzer_views.my_order, name="my_order"),
    path('myorder_download_invoice/', benutzer_views.myorder_download_invoice, name="myorder_download_invoice"),
    path('marke_model/', benutzer_views.marke_model, name="marke_model"),
    # path('information_page/', benutzer_views.information_page, name="information_page"),
    path('terms-and-conditions/', benutzer_views.terms_condition, name="terms_condition"),
    path('allgemeine_daten_get/', benutzer_views.kundendaten_get, name="kundendaten_get"),
    path('', include('schadensrechnung.urls'), name="home"),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('post_api/', include("post_api.urls")), 
    re_path(r'^\.well-known/acme-challenge/(?P<path>.*)$', serve, {'document_root': '/var/www/fixmeinhandy/.well-known/acme-challenge'}),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if 'grappelli' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('grappelli/', include('grappelli.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)