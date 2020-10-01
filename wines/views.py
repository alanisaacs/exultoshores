#!/usr/bin/env python3

"""Create web views for the Wine App"""

import sys
from flask import (Flask,
                   render_template,
                   session as login_session,
                   url_for,
                   request,
                   redirect)
from sqlalchemy import (create_engine,
                        asc)
from sqlalchemy.orm import sessionmaker
from models import (Base,
                    Sommelier,
                    Country,
                    Region,
                    Wine)

# Create Flask app
app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('postgresql://winedbuser:winedbuser@localhost/winedb')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# Display home web page
@app.route('/')
def showHome():
    """Display home page"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name))
    regions = session.query(Region).order_by(asc(Region.name))
    sommeliers = session.query(Sommelier).order_by(asc(Sommelier.username))
    wines = session.query(Wine)
    session.close()
    return render_template('home.html',
                           countries=countries,
                           regions=regions,
                           sommeliers=sommeliers,
                           wines=wines)


# Create a new country
@app.route('/country/new', methods=['GET', 'POST'])
def newCountry():
    """Create a new country"""
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'])
        session = DBSession()
        session.add(newCountry)
        session.commit()
        session.close()
        return redirect(url_for('showHome'))
    else:
        return render_template('newCountry.html')


# Create a new region
@app.route('/region/new', methods=['GET', 'POST'])
def newRegion():
    """Create a new region"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name))
    if request.method == 'POST':
        newRegion = Region(
            country_id=request.form['country_id'],
            name=request.form['name'])
        session.add(newRegion)
        session.commit()
        session.close()
        return redirect(url_for('showHome'))
    else:
        session.close()
        return render_template('newRegion.html',
                               countries=countries)


# Add a wine to the database
@app.route('/wine/new', methods=['GET', 'POST'])
def newWine():
    """Create a new wine"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name))
    regions = session.query(Region).order_by(asc(Region.name))
    if request.method == 'POST':
        newWine = Wine(
            country_id=request.form['country_id'],
            region_id=request.form['region_id'],
            name=request.form['name'],
            year=request.form['year'],
            price=request.form['price'],
            rating=request.form['rating'],
            abv=request.form['abv'],
            date_tasted=request.form['date_tasted'],
            label_photo=request.form['label_photo'],
            description=request.form['description'],
            sommelier_id=request.form['sommelier_id']
            )
        session.add(newWine)
        session.commit()
        session.close()
        return redirect(url_for('showHome'))
    else:
        session.close()
        return render_template('newWine.html', countries=countries, regions=regions)


if __name__ == '__main__':
    app.secret_key = 'dev_key'
    app.debug = True
    app.run()