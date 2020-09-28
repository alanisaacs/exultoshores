#!/usr/bin/env python3

"""Create database tables for the Wine App"""

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    """Registered user information"""
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    password = Column(String(80))
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
    name = Column(String(250), nullable=False)
    description = Column(String(5000))
    price = Column(Float)
    rating = Column(Integer)
    year = Column(Integer)
    abv = Column(Float)
    date_tasted = Column(Date)
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)
    region_id = Column(Integer, ForeignKey('region.id'))
    region = relationship(Region)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


# Start running on postgresql
engine = create_engine('postgresql://winedbuser:winedbuser@localhost/winedb')

Base.metadata.create_all(engine)
