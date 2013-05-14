from datetime import date, datetime, timedelta

from sqlalchemy import Column, Date, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

from traffic_logging import engine


Base = declarative_base()


class TrafficEvent(Base):
    """
    Class is a data structure representing a single traffic event and its
    mapping to a SQL database table
    """
    __tablename__ = 'TrafficEvent'
    _id = Column(Integer, Sequence('trafficevent_id_seq'), primary_key=True)
    problem_nature = Column(String(50))
    address = Column(String(50))
    zip_code = Column(String(5))
    date = Column(Date)
    time = Column(String(5))
    status = Column(String(50))
    dispatch_channel = Column(String(50))

    def __init__(
            self, problem_nature, address, date,
            time, status, dispatch_channel, zip_code=None):
        self.problem_nature = problem_nature
        self.address = address
        self.zip_code = zip_code
        self.date = date
        self.time = time
        self.status = status
        self.dispatch_channel = dispatch_channel

    def __repr__(self):
        return "<TrafficEvent: {0}, {1}, {2}, {3}, {4}, {5}, {6}>".format(
            self.problem_nature,
            self.address,
            self.zip_code,
            self.date,
            self.time,
            self.status,
            self.dispatch_channel

        )

Base.metadata.create_all(engine)


def parse_traffic_event(traffic_item):
    """
    function parses the text for a traffic item and
    creates a new TrafficEvent object
    """
    traffic_event = TrafficEvent(
        problem_nature=traffic_item[0].get_text(),
        address=traffic_item[1].get_text(),
        time=traffic_item[2].get_text(),
        date=get_traffic_event_date(traffic_item[2].get_text()),
        status=traffic_item[3].get_text(),
        dispatch_channel=traffic_item[4].get_text()
    )
    return traffic_event


def get_traffic_event_date(event_time):
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
