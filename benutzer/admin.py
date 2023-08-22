from django.contrib import admin

# Register your models here.


from .models import Auftrag, AuftragPdfResponseApi

admin.site.register(Auftrag)
admin.site.register(AuftragPdfResponseApi)