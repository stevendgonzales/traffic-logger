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








