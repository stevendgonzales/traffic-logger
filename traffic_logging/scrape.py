import time

from bs4 import BeautifulSoup
import requests

from traffic_logging import Session
import traffic_logging.geocode_api as geocode_api
from traffic_logging.data.traffic import parse_traffic_event, TrafficEvent

#create a new database session
session = Session()

#make a web request for the traffic data web site
response = requests.get('https://webapps2.sanantonio.gov/traffic/Traffic.aspx')
html_text = response.text

#turn the html text form the requested site into a beautiful soup object
#and parse out the grid related to traffic data
soup = BeautifulSoup(html_text)
grid_outer = soup.find(id="GridView1")
grid_inner = grid_outer.find_all("tr")

#create a list of TrafficEvent objects from the data
# retrieved from the web request
traffic_events = [parse_traffic_event(row.find_all("td"))
                  for row in grid_inner if len(row.find_all("td")) > 4]


for traffic_event in traffic_events:
    print traffic_event
    existing_traffic_event = session.query(TrafficEvent).filter_by(
        address=traffic_event.address,
        time=traffic_event.time,
        date=traffic_event.date
    ).first()
    print 'existing event: '
    print existing_traffic_event

    if not existing_traffic_event:
        print 'adding_event'
        session.add(traffic_event)
        session.commit()
    else:
        print 'event already added'


    #geo_data = Geocoder.geocode("{0} San Antonio, Texas".format(traffic_event.address))
    #print geo_data[0].postal_code
