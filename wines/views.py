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
                        desc,
                        null,
                        update)
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


# Display all the wines in the db on the home page
@app.route('/')
def showHome():
    """Display home page"""
    session = DBSession()
    # QUERY so that result is a list with element 0 a Wine object
    # and the other three elements are the relations to it.
    # Note that sommelier_id could be None (NULL in DB) so 
    # we need an outer join to keep the Wine object in that case
    wines = session.query(Wine, Country.name, Region.name, Sommelier.username).join(
                        Country, Wine.country_id==Country.id).join(
                        Region, Wine.region_id==Region.id).outerjoin(
                        Sommelier, Wine.sommelier_id==Sommelier.id).order_by(
                        desc(Wine.id)).all()
    session.close()
    # Replace new line (\r\n) characters in description with <br>
    for wine in wines:
        s = (wine[0].description)
        if s: # filter out null values
            s = s.replace("\r\n", "<br>")
            wine[0].description = s
    return render_template('home.html',
                           wines=wines)


# Display a table of all wines for editing purposes
@app.route('/wineTable')
def showWineTable():
    """Display wine table"""
    session = DBSession()
    # QUERY so that result is a list with element 0 a Wine object
    # and the other two elements are the relations to it.
    wines = session.query(Wine, Country.name, Region.name).join(
                        Country, Wine.country_id==Country.id).join(
                        Region, Wine.region_id==Region.id).order_by(
                        desc(Wine.id)).all()
    session.close()
    return render_template('wineTable.html',
                          wines=wines)


# Display a single wine for editing
@app.route('/showOneWine', methods=['GET', 'POST'])
def showOneWine():
    """Display a single wine"""
    if request.method == 'POST':
        session = DBSession()
        # QUERY one wine by id; result is a Wine object
        wineToEdit = session.query(Wine).\
            filter(Wine.id == request.form['wineid']).\
            one_or_none()
        session.close()
        # can't iterate through single wine in template
        # so copying attributes (vars) into a dictionary
        wineDict = {}
        wineDict = (vars(wineToEdit))
        # remove var that isn't part of data
        wineDict.pop('_sa_instance_state')
        # treat description separately to display on top of page
        wineDescription = wineDict.pop('description')
        # display any None (null) values as blank spaces
        # then it is easy to convert them to NULL again
        # on their way back to the database
        # (see newwine view)
        for w in wineDict:
            if wineDict[w] == None:
                wineDict[w] = ""
        return render_template('showOneWine.html', 
            wineToEdit=wineDict, wineDescription=wineDescription)
    else:
        print("======= IN SHOWONEWINE GET ======= ")
        return render_template('showOneWine.html')

    
# Update wine record with values from showOneWine view
@app.route('/updateWine', methods=['GET', 'POST'])
def updateWine():
    """Update a wine record"""
    if request.method == 'POST':
        # Convert blank strings in form to None (NULL)
        # TODO: consolidate with new wine view
        fields = {}
        for i, j in request.form.items():
            if j:
                fields[i] = j
            else:
                fields[i] = None
        session = DBSession()
        # QUERY the wine record by id
        # note the result is itself a query
        wineToUpdate = session.query(Wine).\
            filter(Wine.id==request.form['id'])
        # update everything in the form
        # TODO: only update changed items
        for i in fields:
            wineToUpdate.update({
                i: fields[i]
            })
        session.commit()
        # QUERY again wine by id, closing transaction this time
        wineToEdit = session.query(Wine).\
            filter(Wine.id == request.form['id']).\
            one_or_none()
        session.close()
        # copy to dict like in showOneWine
        # TODO: consolidate into function
        wineDict = {}
        wineDict = (vars(wineToEdit))
        wineDict.pop('_sa_instance_state')
        # TODO: also consolidate this
        for w in wineDict:
            if wineDict[w] == None:
                wineDict[w] = ""
        wineDescription = wineDict.pop('description')
        return render_template('showOneWine.html', wineToEdit=wineDict, wineDescription=wineDescription)
    else:
        print("======= IN UPDATEWINE GET ======= ")
        # need to grab values from db as in showOneWine if this is ever called
        return render_template('showOneWine.html')


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
        # this should never happen
        return render_template('manageCountryRegion.html')


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
        return render_template('manageCountryRegion.html')


# Add a wine to the database
@app.route('/wine/new', methods=['GET', 'POST'])
def newWine():
    """Create a new wine"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name)).all()
    regions = session.query(Region).order_by(asc(Region.name)).all()
    # Replace any empty strings in the form fields with <None> 
    # Note: <None> is inserted into the db as NULL
    # Note: <None> will display in html as the string "None" by default
    fields = {}
    if request.method == 'POST':
        for i, j in request.form.items():
            if j:
                fields[i] = j
            else:
                fields[i] = None
        # print("FIELDS = %s" % fields)
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