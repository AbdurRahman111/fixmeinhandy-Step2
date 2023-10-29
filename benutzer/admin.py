# Register your models here.
from django.contrib import admin
from .models import Auftrag, AuftragPdfResponseApi, MarkeTable, ModelTable, SchadensartTable, Ausgeführter_Befehl



def Complete_status(modeladmin, request, queryset):
    for obj in queryset:
        obj.Auftrag_status = 'Completed'
        obj.save()
Complete_status.short_description = "status to Completed"
class Auftrag_show(admin.ModelAdmin):
    readonly_fields = ['serial_number', 'sequence_number']
    # list_display = ['id', 'User', 'email', 'vorname', 'nachname', 'geburtsdatum', 'Adresszeile', 'Hausnummer', 'Stadt', 'marke', 'model', 'Schadensart', 'screen_protector_status' ,'kosten', 'telefon', 'Auftrag_status', 'Zeit']
    search_fields = ['sequence_number', 'id', 'User__username', 'email', 'vorname', 'nachname', 'geburtsdatum', 'Adresszeile', 'Hausnummer', 'Stadt', 'marke', 'model', 'Schadensart', 'telefon', 'Auftrag_status', 'Zeit']
    actions = [Complete_status]
admin.site.register(Auftrag, Auftrag_show)


class Ausgeführter_Befehl_show(admin.ModelAdmin):
    readonly_fields = ['serial_number', 'sequence_number']
    # list_display = ['id', 'User', 'email', 'vorname', 'nachname', 'geburtsdatum', 'Adresszeile', 'Hausnummer', 'Stadt', 'marke', 'model', 'Schadensart', 'screen_protector_status' ,'kosten', 'telefon', 'Auftrag_status', 'Zeit']
    search_fields = ['id', 'User__username', 'email', 'vorname', 'nachname', 'geburtsdatum', 'Adresszeile', 'Hausnummer', 'Stadt', 'marke', 'model', 'Schadensart', 'telefon', 'Auftrag_status', 'Zeit']
admin.site.register(Ausgeführter_Befehl, Ausgeführter_Befehl_show)


class AuftragPdfResponseApi_show(admin.ModelAdmin):
    list_display = ['id', 'Auftrag']
admin.site.register(AuftragPdfResponseApi, AuftragPdfResponseApi_show)


class models_in_marke(admin.TabularInline):
    model = ModelTable  # Specify the related model
    extra = 1  # Number of empty forms to display
class Schadensart_in_models(admin.TabularInline):
    model = SchadensartTable  # Specify the related model
    extra = 1  # Number of empty forms to display
class MarkeTable_show(admin.ModelAdmin):
    inlines = [models_in_marke]
    list_display = ['Serial_Number', 'Name']
    search_fields = ['id', 'Name']
    ordering = ['Serial_Number']
admin.site.register(MarkeTable, MarkeTable_show)


class ModelTable_show(admin.ModelAdmin):
    inlines = [Schadensart_in_models]
    list_display = ['Name', 'Marke']
    search_fields = ['id', 'Marke__Name', 'Name']
admin.site.register(ModelTable, ModelTable_show)


class SchadensartTable_show(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Price']
    search_fields = ['id', 'Name']
# admin.site.register(SchadensartTable, SchadensartTable_show)