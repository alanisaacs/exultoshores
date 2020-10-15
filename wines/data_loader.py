#!/usr/bin/env python3

"""Populate sample data into the Wine App"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from models import Sommelier, Country, Region, Wine
 
 # Connect to database
engine = create_engine('postgresql://winedbuser:winedbuser@localhost/winedb')
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add default user
sommelier1 = Sommelier(
    username = "Default_Sommelier",
    password = "Default",
    email = "default@exultoshores.com",
    picture = "https://img.webmd.com/dtmcms/live/webmd/consumer_assets/site_images/article_thumbnails/other/cat_relaxing_on_patio_other/1800x1200_cat_relaxing_on_patio_other.jpg"
)

session.add(sommelier1)
session.commit()

# Set up countries
country1 = Country(name = "France")
country2 = Country(name = "Italy")

session.add(country1)
session.add(country2)
session.commit()


# Set up regions
region1 = Region(
    name = "Burgundy",
    country_id = 1,
    country = country1
    )
region2 = Region(
    name = "Bordeaux",
    country_id = 1,
    country = country1
    )

session.add(region1)
session.add(region2)
session.commit()


# Add a wine
wine1 = Wine(
    name = "Dubois Bernard & Fils Chorey-les-Beaune \"Clos Margot\"", 
    description = "Leather coin purse, beef jerky, with copper pennies. Blackberry compost.\r\n\r\nNice structure, though acidity fades into the distance with an unexpected pithy aftertaste (\"till the diminution of space had pointed him sharp as my needle\"—Cymbeline I.3.23).\r\n\r\n Pairs with rack of lamb with cocoa rub, or duck with berry compote.", 
    appellation = "Chorey-les-Beaune",
    price = 33.99, 
    rating = 89, 
    year = 2017,
    abv = 13.0,
    date_tasted = "2020-08-20",
    times_tasted = 1,
    label_photo = None,
    purchased_at = None,
    country_id = 1, 
    country = country1,
    region_id = 1,
    region = region1,
    sommelier_id = 1,
    sommelier = sommelier1
    )
session.add(wine1)
session.commit()


print('Wine data added.')