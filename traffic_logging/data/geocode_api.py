import requests


def request_geocode_json(address):
    base_uri = "http://maps.googleapis.com/maps/api/geocode/json"
    uri = "{0}?address={1}&sensor=false".format(
        base_uri, address.replace(" ", "+"))
    print uri
    response = requests.get(uri)
    return response.json()


def get_zip_code(traffic_event):
    geocode_data = request_geocode_json(
        "{0} San Antonio, Texas".format(traffic_event.address))
    print geocode_data
    address_components = geocode_data['results'][0]['address_components']

    for address_component in address_components:
        if "postal_code" in address_component["types"]:
            return address_component["short_name"]
    return None
