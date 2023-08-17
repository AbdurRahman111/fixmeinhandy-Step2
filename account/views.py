from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import User_Profile


def registration(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

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

            # create user
            myuser = User.objects.create_user(email, email, password)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.is_active = True
            myuser.save()

            # user = authenticate(username=email, password=password)
            login(request, myuser)

            messages.success(request, f'Your account has been created !!! you are now logged in as {first_name} {last_name}')

            return redirect('/')

        else:
            value_dic = {'first_name': first_name, 'last_name': last_name, 'email': email, 'erorr_message': erorr_message}
            return render(request, 'account/registration.html', value_dic)


    return render(request, 'account/registration.html')




def logout_func(request):
    # this is for logout from user id
    logout(request)
    return redirect('/')


def login_func(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        log_password = request.POST.get('password')
        # this is for authenticate username and password for login
        user = authenticate(username=email, password=log_password)

        erorr_message_2 = ""

        if user is not None:
            login(request, user)
            # messages.success(request, "Successfully Logged In !!")
            return redirect('/')
        else:
            erorr_message_2 ="Invalid Credentials, Please Try Again !!"

            value_func2 = {'erorr_message_2':erorr_message_2, 'email':email}
            # messages.error(request, "Invalid Credentials, Please Try Again !!")
            return render(request, 'account/login_page.html', value_func2)
    else:
        return render(request, "account/login_page.html")

def my_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            vorname = request.POST.get('vorname')
            nachname = request.POST.get('nachname')
            # email = request.POST.get('email')
            telefon = request.POST.get('telefon')
            ort = request.POST.get('ort')
            Adresszeile = request.POST.get('Adresszeile')
            Hausnummer = request.POST.get('Hausnummer')
            Stadt = request.POST.get('Stadt')
            Postleitzahl = request.POST.get('Postleitzahl')
            if not Postleitzahl:
                Postleitzahl = None
            geburtsdatum = request.POST.get('geburtsdatum')
            if geburtsdatum:
                date_obj = datetime.datetime.strptime(geburtsdatum, "%d.%m.%Y").date()
            else:
                date_obj = None
            if User_Profile.objects.filter(user=request.user):
                get_profile = User_Profile.objects.get(user=request.user)
                get_profile.geburtsdatum=geburtsdatum
                get_profile.ort=ort
                get_profile.Adresszeile=Adresszeile
                get_profile.Hausnummer=Hausnummer
                get_profile.Stadt=Stadt
                get_profile.Postleitzahl=Postleitzahl
                get_profile.telefon=telefon
                get_profile.save()
                get_profile.user.first_name = vorname
                get_profile.user.last_name = nachname
                get_profile.user.save()
            else:
                var_User_Profile = User_Profile(user=request.user, geburtsdatum=geburtsdatum, ort=ort, Adresszeile=Adresszeile, Hausnummer=Hausnummer, Stadt=Stadt, Postleitzahl=Postleitzahl, telefon=telefon)
                var_User_Profile.save()

                var_User_Profile.user.first_name = vorname
                var_User_Profile.user.last_name = nachname
                var_User_Profile.user.save()

            messages.success(request, "Profile Updated")
            return redirect('/account/my_profile/')
        else:
            if User_Profile.objects.filter(user=request.user):
                get_profile = User_Profile.objects.get(user=request.user)
            else:
                get_profile = None
            context = {'get_profile':get_profile}
            return render(request, "account/my_profile.html", context)
    return redirect('/')