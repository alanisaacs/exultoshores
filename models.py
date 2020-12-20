#!/usr/bin/env python3

"""Manage database and models for EOS"""

import os
import urllib.parse

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Sommelier(Base):
    """Registered user information"""
    __tablename__ = 'sommelier'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    password = Column(String(1024))
    email = Column(String(250))
    picture = Column(String(500))


class Country(Base):
    """Each wine is associated with a country"""
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Region(Base):
    """Each wine is associated with a region"""
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)


class Wine(Base):
    """Data for each wine"""
    __tablename__ = 'wine'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(5000))
    appellation = Column(String(64))
    price = Column(Float(2))
    rating = Column(Integer)
    year = Column(Integer)
    abv = Column(Float(1))
    date_tasted = Column(Date)
    times_tasted = Column(Integer)
    label_photo = Column(String(128))
    purchased_at = Column(String(64))
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    country = relationship(Country)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    region = relationship(Region)
    sommelier_id = Column(Integer, ForeignKey('sommelier.id'))
    sommelier = relationship(Sommelier)


# Start running on postgresql
# Get db user password from environment variable and encode as URI safe
# THIS WORKS FINE LOCALLY USING ENV FROM .BASH_PROFILE
pw = os.getenv('WINE_DB_USER_PW')
pw_encoded = urllib.parse.quote_plus(pw)
engine = create_engine('postgresql://winedbuser:' + pw_encoded + '@localhost/winedb')

Base.metadata.create_all(engine)

########## DEBUGGING ONLY ##########
# import logging
# logging.warning("===== SQLALCHEMY LOGGING IS ON =====")
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO) 
####################################


# If running as a module provide session opener
if __name__ != '__main__':
    open_db_session = sessionmaker(bind=engine)
    # ---- To open session use this syntax ----
    # from models import open_db_session
    # DBSession = openDBSession()

# If running as a script create models only
if __name__ == '__main__':
    print("Models created.")