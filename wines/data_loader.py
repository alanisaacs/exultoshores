#!/usr/bin/env python3

"""Populate sample data into the Wine App"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import User, Country, Region, Wine
 
 # Connect to database
engine = create_engine('postgresql://winedbuser:winedbuser@localhost/winedb')
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add default user
user1 = User(
    username = "Default",
    password = "Default",
    email = "default@exultoshores.com",
    picture = "https://photos.app.goo.gl/Z9ytt5motCPeHaHk9"
)

session.add(user1)
session.commit()

# Set up countries
country1 = Country(name = "France")
country2 = Country(name = "Italy")
country3 = Country(name = "USA")

session.add(country1)
session.add(country2)
session.add(country3)
session.commit()


# Set up regions
region1 = Region1(
    name = "Burgundy",
    country_id = 1,
    country = country1
    )
region2 = Region2(
    name = "Bordeaux"
    country_id = 1,
    country = country1
    )
region3 = Region3(
    name = "Chianti"
    country_id = 2,
    country = country2
    )

session.add(region1)
session.add(region2)
session.add(region3)
session.commit()


# Add a wine
wine1 = Wine(
    name = "Bois-Malot, Bordeaux Sup\u00e9rieur", 
    description = "K&L: Located in St-Loubes and situated on the shoreline of the Dordogne River. The soils are clay and light limestone with a subsoil of red pebbles and clay. The blend is 50% Cabernet Sauvignon, 30% Merlot, and 20% Cabernet Franc. It was aged for 18 months in large vats and then an additional 6 months in oak.", 
    price = 29.99, 
    rating = 90, 
    year = 2017,
    abv = 13.5,
    date_tasted = "2020-09-22"
    country_id = 1, 
    country = country1,
    region_id = 2,
    region = region2,
    user_id = 1,
    user = user1
    )
session.add(wine1)
session.commit()


print('Wine data added.')