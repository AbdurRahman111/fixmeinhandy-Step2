from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import os
from django.conf import settings
from benutzer.forms import KundendatenForm
# request handler
# request -> response
from urllib.parse import parse_qs


def schadensrechnung(request):
    # Pull data
    # Transform data
    # send emails

    return render(request, 'schadensrechnung/home.html', {'name': 'Mosh'})


def get_handy_namen(request):
    marke = request.GET.get('selected_value')
    fp = open(os.path.join(settings.BASE_DIR, 'schadensrechnung/static/schadensrechnung/json/marken_namen.json'))
    marken_namen = json.load(fp)
    # print("Marke:", marke)
    modelle = marken_namen[marke]


    options = [{'value': '0', 'label': 'Bitte wählen Sie ein Model ...'}]
    for name in modelle:
        options.append({'value': name, 'label': name})

    return JsonResponse({'options': options})




def get_schadensart(request):
    model = request.GET.get('selected_value')
    fp = open(os.path.join(settings.BASE_DIR, 'schadensrechnung/static/schadensrechnung/json/preise.json'))
    preise = json.load(fp)
    # print("model:", model)
    # print(preise)
    modelle = preise[model]

    options = [{'value': '0', 'label': 'Bitte wählen Sie die Schadensart ...'}]
    for key, value in modelle.items():
        # print(key, value)
        options.append({'value': value, 'label': key})
    return JsonResponse({'options': options})







def get_preis(request):
    schadensart = request.GET.get('selected_value')
    model = request.GET.get('model')

    print(schadensart, model)
    
    no_select_flag = 0
    sonstiges_flag = 0
    preis = -1

    if schadensart == '0':
        no_select_flag = 1
    elif schadensart == '14':
        sonstiges_flag = 1
    else:
        # Konvertieren Sie den Modellnamen in Kleinbuchstaben für den Groß-/Kleinschreibung-unsensiblen Vergleich
        correct_case_model = model.title()


        # Laden Sie die JSON-Datei mit den Modellnamen in Kleinbuchstaben
        fp = open(os.path.join(settings.BASE_DIR, 'schadensrechnung/static/schadensrechnung/json/preise.json'))
        preisliste = json.load(fp)

        # Holen Sie den Preis unter Verwendung des Modellnamens in Kleinbuchstaben
        preis = preisliste[correct_case_model][SCHADENCODE[schadensart]]

    response_data = {
        'sonstiges': sonstiges_flag,
        'preis': preis,
        'no_select': no_select_flag
        }

    return JsonResponse(response_data)

    


SCHADENCODE = {
    '1': "Display & Touchscreen",
    '2': "Akku bzw. Batterieaustausch",
    '3': "Ladestecker bzw. Ladebuchse",
    '4': "Ohrlautsprecher",
    '5': "Mikrofon",
    '6': "Hauptkamera",
    '7': "Frontkamera (Selfie)",
    '8': "Kamera-Glas (Abdeckung-Rückseite)",
    '9': "Klingeltonlautsprecher",
    '10': "Kopfhöreranschluss",
    '11': "Wasserschaden Erstdiagnose",
    '12': "Fehleranalyse & Kostenvoranschlag",
    '13': "Software Fehler",
    '14': "Sonstige Reparaturen"
}


def Impressum(request):
    return render(request, 'schadensrechnung/Impressum.html')

def Datenschutzerklarung(request):
    return render(request, 'schadensrechnung/Datenschutzerklarung.html')