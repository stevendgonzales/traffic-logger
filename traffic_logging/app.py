from traffic_logging import Session
from traffic_logging.data.utils import (
    event_already_exist, find_zip_code, save_traffic_event)
from traffic_logging.web import scrape


#create a new database session
session = Session()

#scrape the city of san antonio website for traffic vents
traffic_events = scrape.get_traffic_events()

for traffic_event in traffic_events:
    if not event_already_exist(session, traffic_event):
        traffic_event.zip_code = find_zip_code(session, traffic_event)
        save_traffic_event(session, traffic_event)
        print 'event added'
    else:
        print 'event already added'
