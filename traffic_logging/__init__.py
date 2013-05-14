from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#initialize the application's database engine and create a sessionmaker
engine = create_engine('sqlite:///traffic.db', echo=True)
Session = sessionmaker(bind=engine)

