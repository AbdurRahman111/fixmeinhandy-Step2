from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponse
from .forms import KundendatenForm
from django.contrib import messages
from .soap_client import create_soap_client, create_shipment_request
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import datetime
from post_api.views import api_to_pdf
from .models import Auftrag, AuftragPdfResponseApi
from account.models import User_Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from io import BytesIO


def marke_model(request):
    if request.method == "POST":
        marke = request.POST.get('marke')
        model = request.POST.get('model')
        art = request.POST.get('art')
        art_array = art.split(",")
        # print(art_array)
        # print(art_array[0])
        # print(art_array[1])
        preis_input = request.POST.get('preis_input')
        # print(art)
        # print('artart')

        # if art == '1':
        #     main_art = 'Display & Touchscreen'
        # elif art == '2':
        #     main_art = 'Akku'
        # elif art == '3':
        #     main_art = 'Ladebuchse'
        # elif art == '4':
        #     main_art = 'Rückglas'
        # else:
        #     main_art = 'Sonstiges'

        # print(marke, model, main_art)
        form = KundendatenForm()

        try:
            get_profile = User_Profile.objects.get(user=request.user)
        except:
            get_profile = None

        context = {'marke':marke, 'model':model, 'art':art_array[1], 'form':form, 'preis_input':preis_input, 'get_profile': get_profile}
        return render(request, 'benutzer/kundendaten.html', context)

    else:
        return redirect('/')


def terms_condition(request):
    # send_mail(
    #     'Ihr Reparaturauftrag bei FixMeinHandy',  # subject of mail
    #     'email_body',  # body of mail
    #     'office@fixmeinhandy.at',  # Your email address
    #     ['suvosorkar7uu8@gmail.com'],  # Recipient email address(es)
    #     fail_silently=False,
    # )
    return render(request, "benutzer/terms_condition.html")


def my_order(request):
    if request.user.is_authenticated:
        my_order = Auftrag.objects.filter(User=request.user).order_by('-id')
        context = {'my_order':my_order}
        return render(request, "benutzer/my_order.html", context)
    else:
        return redirect('/')

def myorder_download_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            Auftrag_id = request.POST.get('Auftrag_id')
            # print('paglu test')
            # print(Auftrag_id)

            get_Response_Of_PDF = AuftragPdfResponseApi.objects.get(Auftrag=Auftrag.objects.get(id = Auftrag_id))
            buffer = BytesIO(get_Response_Of_PDF.response)
            response = FileResponse(buffer, as_attachment=True, filename='sendung.pdf')
            return response
    else:
        return redirect('/')


def kundendaten_get(request):
    if request.method == 'POST':
        vorname = request.POST.get('vorname')
        nachname = request.POST.get('nachname')
        email = request.POST.get('email')
        telefon = request.POST.get('telefon')
        # ort = request.POST.get('ort')
        Adresszeile = request.POST.get('Adresszeile')
        Hausnummer = request.POST.get('Hausnummer')
        Stadt = request.POST.get('Stadt')
        Postleitzahl = request.POST.get('Postleitzahl')
        marke = request.POST.get('marke')

        model = request.POST.get('model')
        art = request.POST.get('art')

        preis_input = request.POST.get('preis_input')

        geburtsdatum = request.POST.get('geburtsdatum')
        # date_obj = datetime.datetime.strptime(geburtsdatum, "%d.%m.%Y").date()

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        var_Auftrag = Auftrag(email=email, vorname=vorname, nachname=nachname, geburtsdatum=geburtsdatum, Adresszeile=Adresszeile, Hausnummer=Hausnummer, Stadt=Stadt, Postleitzahl=Postleitzahl, marke=marke, model=model, Schadensart=art, kosten=preis_input, telefon=telefon)
        var_Auftrag.save()

        if request.user.is_authenticated:
            var_Auftrag.User = request.user
            var_Auftrag.save()

        email = var_Auftrag.email
        first_name = var_Auftrag.vorname
        last_name = var_Auftrag.nachname
        # print(username, email, first_name, last_name)

        if password:
            # check the error inputs
            user_username_info = User.objects.filter(username=email)
            user_email_info = User.objects.filter(email=email)

            erorr_message = ""

            if user_username_info:
                # messages.error(request, "Username Already Exist")
                erorr_message = "Email is Already Exist"

            elif user_email_info:
                # messages.error(request, "Email Already Exist")
                erorr_message = "Email is Already Exist"

            elif password != confirm_password:
                # messages.error(request, "Passwords are not match")
                erorr_message = "Passwords are not match!"

            elif len(password) < 8:
                # messages.error(request, "Passwords Must be Al least 7 Digits")
                erorr_message = "Passwords Must be Al least 8 Digits"

            if not erorr_message:
                print('ssss')
                print(first_name, last_name)
                # create user
                myuser = User.objects.create_user(email, email, password)
                if last_name:
                    myuser.first_name = first_name
                else:
                    myuser.first_name = ''

                if last_name:
                    myuser.last_name = last_name
                else:
                    myuser.last_name = ''
                myuser.is_active = True
                myuser.save()

                # user = authenticate(username=email, password=password)
                login(request, myuser)

                if request.user.is_authenticated:
                    var_Auftrag.User = request.user
                    var_Auftrag.save()

                    if not User_Profile.objects.filter(user=request.user):
                        get_profile = User_Profile(user=request.user, telefon=telefon, geburtsdatum=geburtsdatum, Adresszeile=Adresszeile, Hausnummer=Hausnummer, Stadt=Stadt, Postleitzahl=Postleitzahl)
                        get_profile.save()
                messages.success(request,
                                 f'Your account has been created !!! you are now logged in as {first_name} {last_name}')

                email_body = render_to_string(
                    'benutzer/order_email.html',
                    {
                        'first_name': var_Auftrag.vorname,
                        'last_name': var_Auftrag.nachname,
                        'email': var_Auftrag.email,
                        'product': str(var_Auftrag.marke) + " " + str(var_Auftrag.model),
                        'total_bill': var_Auftrag.kosten,
                        'full_address': str(var_Auftrag.Adresszeile) + " " + str(var_Auftrag.Hausnummer) + " " + str(
                            var_Auftrag.Stadt) + " " + str(var_Auftrag.Postleitzahl),
                        'city': var_Auftrag.Stadt,
                        'postal_code': var_Auftrag.Postleitzahl,
                        'phone': var_Auftrag.telefon,
			            'marke': var_Auftrag.marke,
                	    'model': var_Auftrag.model,
                	    'Schadensart': var_Auftrag.Schadensart,
                    }
                )

                send_mail(
                    'Ihr Reparaturauftrag bei FixMeinHandy',  # subject of mail
                    email_body,  # body of mail
                    'office@fixmeinhandy.at',  # Your email address
                    [var_Auftrag.email],  # Recipient email address(es)
                    fail_silently=True,
                )


                context = {'Adresszeile': var_Auftrag.Adresszeile, 'Hausnummer': var_Auftrag.Hausnummer,
                           'Stadt': var_Auftrag.Stadt, 'Postleitzahl': var_Auftrag.Postleitzahl,
                           'email': var_Auftrag.email,
                           'vorname_nachname': str(var_Auftrag.vorname) + " " + str(var_Auftrag.nachname),
                           'Auftrag_id': var_Auftrag.id}
                return render(request, "benutzer/information_page.html", context)



            else:
                print('okok')
                form = KundendatenForm()
                value_dic = {'erorr_message': erorr_message, 'marke':marke, 'model':model, 'art':art, 'preis_input':preis_input, 'form':form}
                return render(request, 'benutzer/kundendaten.html', value_dic)

        messages.success(request, f'Order created for {var_Auftrag.vorname} {var_Auftrag.nachname}!')

        email_body = render_to_string(
            'benutzer/order_email.html',
            {
                'first_name': var_Auftrag.vorname,
                'last_name': var_Auftrag.nachname,
                'email': var_Auftrag.email,
                'product': str(var_Auftrag.marke)+ " " + str(var_Auftrag.model),
                'total_bill': var_Auftrag.kosten,
                'full_address' : str(var_Auftrag.Adresszeile) + " " + str(var_Auftrag.Hausnummer) + " " + str(var_Auftrag.Stadt) + " " + str(var_Auftrag.Postleitzahl),
                'city' : var_Auftrag.Stadt,
                'postal_code' :var_Auftrag.Postleitzahl,
                'phone' : var_Auftrag.telefon,
		        'marke': var_Auftrag.marke,
                'model': var_Auftrag.model,
                'Schadensart': var_Auftrag.Schadensart,
            }
        )

        if request.user.is_authenticated:
            if not User_Profile.objects.filter(user=request.user):
                get_profile = User_Profile(user=request.user, telefon=telefon, geburtsdatum=geburtsdatum,
                                           Adresszeile=Adresszeile, Hausnummer=Hausnummer, Stadt=Stadt,
                                           Postleitzahl=Postleitzahl)
                get_profile.save()

        send_mail(
            'Ihr Reparaturauftrag bei FixMeinHandy', #subject of mail
            email_body, # body of mail
            'office@fixmeinhandy.at',  # Your email address
            [var_Auftrag.email],  # Recipient email address(es)
            fail_silently=True,
        )

        context = {'Adresszeile':var_Auftrag.Adresszeile, 'Hausnummer':var_Auftrag.Hausnummer, 'Stadt':var_Auftrag.Stadt, 'Postleitzahl':var_Auftrag.Postleitzahl, 'email':var_Auftrag.email, 'vorname_nachname':str(var_Auftrag.vorname)+" "+str(var_Auftrag.nachname), 'Auftrag_id':var_Auftrag.id}

        return render(request, "benutzer/information_page.html", context)

    else:
        form = KundendatenForm()
        context = {'form':form}
        return render(request,'benutzer/kundendaten.html', context)



def kundendaten(request):
    if request.method == 'POST':
        form = KundendatenForm(request.POST)
        print(form)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = KundendatenForm()
    return redirect(request, 'benutzer/kundendaten.html', {'form': form})





def send_soap_request():
    try:
        soap_client = create_soap_client()
        shipment_request = create_shipment_request()

        # Replace 'ImportShipment' with the name of the operation you want to call
        response = soap_client.service.ImportShipment(shipment_request)

        # Process the SOAP response if needed
        # response_data = response['post:ResponseData']
        # ...

        return response
    except Exception as e:
        # Handle any exceptions that might occur during the SOAP request
        # ...
        return None
