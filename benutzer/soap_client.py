from zeep import Client
from zeep.transports import Transport

def create_soap_client():
    # Replace 'http://postag.example.com/soap-endpoint' with the actual PostAG SOAP service endpoint URL
    soap_client = Client(
        'http://postag.example.com/soap-endpoint',
        transport=Transport(http_auth=('your_username', 'your_password'))
    )
    return soap_client

def create_shipment_request():
    # Create the shipment request dictionary based on the PostAG API documentation
    shipment_request = {
        # Fill in the required fields and data for the shipment request
        # ...
    }
    return shipment_request