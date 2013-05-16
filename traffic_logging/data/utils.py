from datetime import date, datetime, timedelta

from traffic_logging.data.traffic import TrafficEvent
from traffic_logging.data import geocode_api


def parse_traffic_event(traffic_item):
    """
    function parses the text for a traffic item and
    creates a new TrafficEvent object
    """
    traffic_event = TrafficEvent(
        problem_nature=traffic_item[0].get_text(),
        address=traffic_item[1].get_text(),
        time=traffic_item[2].get_text(),
        date=_get_traffic_event_date(traffic_item[2].get_text()),
        status=traffic_item[3].get_text(),
        dispatch_channel=traffic_item[4].get_text()
    )
    return traffic_event


def _get_traffic_event_date(event_time):
    """
    Function analyzes the traffic event to determine the date of the event.
    This is necessary since the source of traffic events only includes the time
    """
    event_hour = int(event_time[0:2])
    now = datetime.now()

    #set the date to be today's date
    event_date = date.today()

    #if the current tome is between 12AM and 3AM, but
    #the event_time is between 9PM and 12AM, then set the date for yesterday
    if now.hour < 3 and event_hour > 21:
        event_date = date.today()-timedelta(days=1)

    return event_date


def save_traffic_event(session, traffic_event):
    session.add(traffic_event)
    session.commit()


def event_already_exist(session, traffic_event):
    existing_traffic_event = session.query(TrafficEvent).filter_by(
        address=traffic_event.address,
        time=traffic_event.time,
        date=traffic_event.date
    ).first()

    if existing_traffic_event:
        return True

    return False


def find_zip_code(session, traffic_event):

    zip_code = session.query(TrafficEvent.zip_code).filter_by(
        address=traffic_event.address,
        time=traffic_event.time,
        date=traffic_event.date
    ).scalar()

    if not zip_code:
        zip_code = geocode_api.get_zip_code(traffic_event)

    return zip_code
