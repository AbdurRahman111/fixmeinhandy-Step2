from django.http import FileResponse, HttpResponse
import xml.etree.ElementTree as ET
import requests
import base64
from io import BytesIO
from django.conf import settings
from benutzer.models import Auftrag, AuftragPdfResponseApi
from django.core.files.base import ContentFile
BASE_DIR = settings.BASE_DIR

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def api_to_pdf(request):
    Auftrag_id = request.POST.get('Auftrag_id')
    get_Auftrag = Auftrag.objects.get(id=Auftrag_id)
    # print(get_Auftrag)
    # Adresszeile = get_Auftrag.Adresszeile
    # Hausnummer = get_Auftrag.Hausnummer
    # Stadt = get_Auftrag.Stadt
    # Postleitzahl = get_Auftrag.Postleitzahl
    # email = get_Auftrag.email
    # vorname_nachname = str(get_Auftrag.vorname)+" "+str(get_Auftrag.nachname)

    StreetName = request.POST.get('StreetName')
    Hausnummer = request.POST.get('Hausnummer')
    Stadt = request.POST.get('Stadt')
    Postleitzahl = request.POST.get('Postleitzahl')
    email = request.POST.get('email')
    vorname_nachname = request.POST.get('vorname_nachname')
    # print('test55')
    # print(StreetName)
    # print(StreetName, Hausnummer, Stadt, Postleitzahl, vorname_nachname, email)
    # Make a request to the API
    response_code, pdf_content = post_api_request(StreetName, Hausnummer, Stadt, Postleitzahl, vorname_nachname, email)
    # print('response_code, pdf_content')
    # print(type(pdf_content))
    # print(response_code, pdf_content)
    # Check if the request was successful
    if response_code == 200:
        # Create a BytesIO buffer to hold the PDF content
        buffer = BytesIO(pdf_content)
        #saving pdf to database
        # content_file = ContentFile(pdf_content)
        # get_Auftrag.PDF_label.save(f'sendung{Auftrag_id}.pdf', content_file)
        # get_Auftrag.save()

        var_Auftrag_Pdf_ResponseApi = AuftragPdfResponseApi(Auftrag=get_Auftrag, response=pdf_content)
        var_Auftrag_Pdf_ResponseApi.save()

        response = FileResponse(buffer, as_attachment=True, filename='sendung.pdf')

        email_body = render_to_string(
            'benutzer/order_email.html',
            {
                'first_name': get_Auftrag.vorname,
                'last_name': get_Auftrag.nachname,
                'email': get_Auftrag.email,
                'product': str(get_Auftrag.marke) + " " + str(get_Auftrag.model),
                'total_bill': get_Auftrag.kosten,
                'full_address': str(get_Auftrag.Adresszeile) + " " + str(get_Auftrag.Hausnummer) + " " + str(
                    get_Auftrag.Stadt) + " " + str(get_Auftrag.Postleitzahl),
                'city': get_Auftrag.Stadt,
                'postal_code': get_Auftrag.Postleitzahl,
                'phone': get_Auftrag.telefon,
                'marke': get_Auftrag.marke,
                'model': get_Auftrag.model,
                'Schadensart': get_Auftrag.Schadensart,
            }
        )
        # send_mail(
        #     'Ihr Reparaturauftrag bei FixMeinHandy',  # subject of mail
        #     email_body,  # body of mail
        #     'office@fixmeinhandy.at',  # Your email address
        #     [get_Auftrag.email],  # Recipient email address(es)
        #     fail_silently=True,
        # )

        # Create an EmailMessage instance
        email = EmailMessage(
            'Ihr Reparaturauftrag bei FixMeinHandy',  # subject of mail
            email_body,  # body of mail (HTML content)
            'office@fixmeinhandy.at',  # Your email address
            [get_Auftrag.email],  # Recipient email address(es)
        )
        # Attach the PDF file to the email
        email.attach('sendung.pdf', response.getvalue(), 'application/pdf')
        # Send the email
        email.send(fail_silently=True)

        buffer = BytesIO(var_Auftrag_Pdf_ResponseApi.response)
        response = FileResponse(buffer, as_attachment=True, filename='sendung.pdf')
        return response
    else:
        return HttpResponse('API Fehler!', status=400)


# Helper Functions

def post_api_request(address_line, house_number, city, postal_code, name, email):
    ET.register_namespace("post", "http://post.ondot.at")
    ET.register_namespace("soapenv", "http://schemas.xmlsoap.org/soap/envelope/")
    print(f'{BASE_DIR}/post_api/templates/post_api/request_leer.xml')
    tree = ET.parse('request_leer.xml')
    root = tree.getroot()
    # printing the root.

    shipper_address_element = root[1][0][0][5]
    for el in shipper_address_element:
        if 'Name1' in el.tag:
            el.text = clean_text(name)
        elif 'City' in el.tag:
            el.text = clean_text(city)
        elif 'AddressLine1' in el.tag:
            el.text = clean_text(address_line)
        elif 'Email' in el.tag:
            el.text = email 
        elif 'PostalCode' in el.tag:
            el.text = postal_code
        elif 'HouseNumber' in el.tag:
            el.text = house_number
    xml = ET.tostring(root)#.decode('utf8') #encoding='utf8'

    url = 'https://plc.post.at/Post.Webservice/ShippingService.svc/secure'
    # url = 'https://abn-plc.post.at/DataService/Post.Webservice/ShippingService.svc/secure'
    #headers = {'content-type': 'application/soap+xml'}
    headers = {
    'Accept-Encoding': 'gzip,deflate',
    'Content-Type': 'text/xml;charset=UTF-8',
    'SOAPAction': 'http://post.ondot.at/IShippingService/ImportShipment',
    'Host': 'plc.post.at',
    'Connection': 'Keep-Alive',
    'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
}
    body = xml

    response = requests.post(url,data=body,headers=headers, verify=False)
    content = response.content 
    content_string = content 

    

    content_tree = ET.ElementTree(ET.fromstring(content_string))

    pdf_data_base64 = find_tag(content_tree, '{http://post.ondot.at}pdfData')
    # print(pdf_data_base64)
    # Decode the base64 data to get the PDF content
    pdf_content = base64.b64decode(pdf_data_base64)
    

    # Save the PDF to a file (you can modify the file name as needed)
    # with open("output.pdf", "wb") as f:
    #     f.write(pdf_content)
    return response.status_code, pdf_content
    # print("PDF extracted and saved as 'output.pdf'")

def find_tag(tree, tag_to_find):
    # Get the root of the XML document
    root = tree.getroot()

    # Iterate over all elements in the document, starting from the root
    for elem in root.iter():
        # If the element's tag is the one we're looking for
        if elem.tag == tag_to_find:
            # Return the element and end the function
            return elem.text

    # If we get through the whole document without finding the tag
    return None


def clean_text(string_text):
    return_string = string_text
    return_string = return_string.replace('ß', 'ss')
    return_string = return_string.replace('ö', 'oe')
    return_string = return_string.replace('ä', 'ae')
    return_string = return_string.replace('ü', 'ue')
    return return_string