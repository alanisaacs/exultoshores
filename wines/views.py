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
                        asc,
                        null)
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


@app.route('/')
def showHome():
    """Display home page"""
    session = DBSession()
    # countries = session.query(Country).order_by(asc(Country.name)).all()
    # regions = session.query(Region).order_by(asc(Region.name)).all()
    # sommeliers = session.query(Sommelier).order_by(asc(Sommelier.username)).all()
    wines = session.query(Wine).all()
    session.close()
    # Replace new line (\r\n) characters in description with <br>
    # print("======= DEBUG DESCRIPTION =======")
    for wine in wines:
        s = (wine.description).replace("\r\n", "<br>")
        # print("s = %s" % s)
        # c = [ letter for letter in s ]
        # print("c = %s" % c)
        wine.description = s
        # print("done replacing")

            
    return render_template('home.html',
                        #    countries=countries,
                        #    regions=regions,
                        #    sommeliers=sommeliers,
                           wines=wines)


# Display a table of all wines for editing purposes
@app.route('/wineTable')
def showWineTable():
    """Display wine table"""
    session = DBSession()
    wines = session.query(Wine).all()
    # countries = session.query(Country).order_by(asc(Country.name))
    # regions = session.query(Region).order_by(asc(Region.name))
    # sommeliers = session.query(Sommelier).order_by(asc(Sommelier.username))
    session.close()
    return render_template('wineTable.html',
                          wines=wines)
                        #   countries=countries,
                        #   regions=regions,
                        #   sommeliers=sommeliers)


# Display a single wine for editing
@app.route('/editWine', methods=['GET', 'POST'])
def editWine():
    """Edit a single wine"""
    if request.method == 'POST':
        print("======= IN POST ======= ")
        print("REQUEST.WINEID = %s" % request.form['wineid'])
        session = DBSession()
        wineToEdit = session.query(Wine).filter(Wine.id == request.form['wineid']).one_or_none()
        session.close()
        # can't iterate through single wine in template
        # so copying into a dictionary
        wineDict = {}
        wineDict = (vars(wineToEdit))
        # print(wineDict)
        return render_template('editWine.html', wineToEdit=wineDict)
    else:
        print("======= IN GET ======= ")
        return render_template('editWine.html')


# Create and edit both countries and regions
@app.route('/manageCountryRegion', methods=['GET', 'POST'])
def manageCountryRegion():
    """Create and edit both countries and regions"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name)).all()
    regions = session.query(Region).order_by(asc(Region.name)).all()
    deletableCountries = session.query(Country).join(Region, full = True).filter(Region.country_id == None).all()
    deletableRegions = session.query(Region).join(Wine, full = True).filter(Wine.region_id == None).all()
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'])
        session.add(newCountry)
        session.commit()
        session.close()
        return redirect(url_for('manageCountryRegion'))
    else:
        session.close()
        return render_template('manageCountryRegion.html',
                           countries=countries,
                           regions=regions,
                           deletableCountries=deletableCountries,
                           deletableRegions=deletableRegions)


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
        return redirect(url_for('manageCountryRegion'))
    else:
        return render_template('newCountry.html')


# Create a new region
@app.route('/region/new', methods=['GET', 'POST'])
def newRegion():
    """Create a new region"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name)).all()
    if request.method == 'POST':
        newRegion = Region(
            country_id=request.form['country_id'],
            name=request.form['name'])
        session.add(newRegion)
        session.commit()
        session.close()
        return redirect(url_for('manageCountryRegion'))
    else:
        session.close()
        return render_template('newRegion.html',
                               countries=countries)


# Add a wine to the database
@app.route('/wine/new', methods=['GET', 'POST'])
def newWine():
    """Create a new wine"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name)).all()
    regions = session.query(Region).order_by(asc(Region.name)).all()
    # Replace any empty strings in the form fields with <None> 
    # Note: <None> is inserted into the db as NULL
    # Note: <None> will display in html as the string "None"
    fields = {}
    if request.method == 'POST':
        for i, j in request.form.items():
            if j:
                fields[i] = j
            else:
                fields[i] = None
        print(fields)
        newWine = Wine(
            country_id=fields['country_id'],
            region_id=fields['region_id'],
            name=fields['name'],
            year=fields['year'],
            price=fields['price'],
            rating=fields['rating'],
            abv=fields['abv'],
            date_tasted=fields['date_tasted'],
            label_photo=fields['label_photo'],
            description=fields['description'],
            sommelier_id=fields['sommelier_id']
            )
        session.add(newWine)
        session.commit()
        session.close()
        return redirect(url_for('showHome'))
    else:
        session.close()
        return render_template('newWine.html', countries=countries, regions=regions)


# Delete an unassociated (no regions or wines) country
@app.route('/deleteCountry', methods=['GET', 'POST'])
def deleteCountry():
    """Delete a country"""
    if request.method == 'POST':
        countryID = request.form['country_id']
        session = DBSession()
        countryToDelete = session.query(Country).filter_by(id=countryID).one_or_none()
        session.delete(countryToDelete)
        session.commit()
        session.close()
        return redirect(url_for('manageCountryRegion'))
    else:
        return render_template('manageCountryRegion.html')


# Delete an unassociated (no wines) region
@app.route('/deleteRegion', methods=['GET', 'POST'])
def deleteRegion():
    """Delete a region"""
    if request.method == 'POST':
        regionID = request.form['region_id']
        session = DBSession()
        regionToDelete = session.query(Region).filter_by(id=regionID).one_or_none()
        session.delete(regionToDelete)
        session.commit()
        session.close()
        return redirect(url_for('manageCountryRegion'))
    else:
        return render_template('manageCountryRegion.html')


# Delete a wine from the wine table
@app.route('/deleteWine', methods=['GET', 'POST'])
def deleteWine():
    """Delete a wine"""
    if request.method == 'POST':
        wineid = request.form['wineid']
        # print("WINEID = %s" % wineid)
        session = DBSession()
        wineToDelete = session.query(Wine).filter_by(id=wineid).one_or_none()
        # print("QUERY COMPLETED WITH: %s" % wineToDelete)
        session.delete(wineToDelete)
        # print("DELETE CALLED. DESCRIPTION: %s" % wineToDelete.description)
        session.commit()
        # print("DELETE COMMITTED NOW")
        session.close()
        # print("DONE WITH DB SESSION")
        return redirect(url_for('showWineTable'))
    else:
        return render_template('wineTable.html')


if __name__ == '__main__':
    app.secret_key = 'dev_key'
    app.debug = True
    app.run()