#!/usr/bin/env python3

"""Create web views for Exult-O-Shores"""

import sys

from flask import (flash,
                   Flask,
                   redirect,
                   render_template,
                   request,
                   session as login_session,
                   url_for)
from sqlalchemy import (asc,
                        desc,
                        null,
                        update)

from auth.routes import auth_bp
from labels.routes import labels_bp
from models import (Base,
                    Country,
                    open_db_session,
                    Region,
                    Sommelier,
                    Wine)

# Create Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(labels_bp)

# Display front end for the whole site
@app.route('/')
def showSiteIndex():
    """Display exultoshores.com index page"""
    return render_template('index.html')


# Display Wine App home page, showing all the wines in the db
@app.route('/wine')
def wineHome():
    """Display Wine App home page"""
    DBSession = open_db_session()
    # QUERY so that result is a list with element 0 a Wine object
    # and the other three elements are the relations to it.
    # Note that sommelier_id could be None (NULL in DB) so 
    # we need an outer join to keep the Wine object in that case
    wines = DBSession.query(Wine, Country.name, Region.name, Sommelier.username).join(
                        Country, Wine.country_id==Country.id).join(
                        Region, Wine.region_id==Region.id).outerjoin(
                        Sommelier, Wine.sommelier_id==Sommelier.id).order_by(
                        desc(Wine.rating)).all()
    DBSession.close()
    # Replace new line (\r\n) characters in description with <br>
    for wine in wines:
        s = (wine[0].description)
        if s: # filter out null values
            s = s.replace("\r\n", "<br>")
            wine[0].description = s
    # If user is logged in pass name to page, otherwise "None"
    userLoggedIn = login_session.get('username')
    return render_template('wine/home.html',
                           wines=wines, userLoggedIn=userLoggedIn)


# Display a table of all wines
@app.route('/wine/table')
def wineTable():
    """Display wine table"""
    DBSession = open_db_session()
    # QUERY so that result is a list with element 0 a Wine object
    # and the other two elements are the relations to it.
    wines = DBSession.query(Wine, Country.name, Region.name).join(
                        Country, Wine.country_id==Country.id).join(
                        Region, Wine.region_id==Region.id).order_by(
                        desc(Wine.id)).all()
    DBSession.close()
    # If user is logged in pass name to page, otherwise "None"
    userLoggedIn = login_session.get('username')
    return render_template('wine/table.html',
                          wines=wines, userLoggedIn=userLoggedIn)


# Display a single wine for editing
@app.route('/wine/wineEdit')
def wineEdit():
    """Display a single wine for editing"""
    # Display wine for editing
    DBSession = open_db_session()
    # QUERY one wine by id (id is passed in query string)
    # Result is a Wine object
    wineid = request.args.get("wineid")
    wineToEdit = DBSession.query(Wine).\
        filter(Wine.id == wineid).\
        one_or_none()
    DBSession.close()
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
    return render_template('wine/wineEdit.html', 
        wineToEdit=wineDict, wineDescription=wineDescription)


# Update wine record with values from wineEdit form view
@app.route('/wine/wineUpdate', methods=['GET', 'POST'])
def wineUpdate():
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
        DBSession = open_db_session()
        # QUERY the wine record by id
        # note the result is itself a query
        wineToUpdate = DBSession.query(Wine).\
            filter(Wine.id==request.form['id'])
        # update everything in the form
        # TODO: only update changed items
        for i in fields:
            wineToUpdate.update({
                i: fields[i]
            })
        DBSession.commit()
        # QUERY again wine by id, closing transaction this time
        wineToEdit = DBSession.query(Wine).\
            filter(Wine.id == request.form['id']).\
            one_or_none()
        DBSession.close()
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
        return redirect(url_for('wineHome'))
    else:
        # Route should only be called with POST
        return render_template('error.html')


# Show counties and regions with create, edit and delete links
@app.route('/wine/countriesRegions', methods=['GET', 'POST'])
def wineCountriesRegions():
    """Manage countries and regions"""
    DBSession = open_db_session()
    countries = DBSession.query(Country).order_by(asc(Country.name)).all()
    regions = DBSession.query(Region).order_by(asc(Region.name)).all()
    deletableCountries = DBSession.query(Country).join(Region, full = True).filter(Region.country_id == None).all()
    deletableRegions = DBSession.query(Region).join(Wine, full = True).filter(Wine.region_id == None).all()
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'])
        DBSession.add(newCountry)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wineCountriesRegions'))
    else:
        DBSession.close()
        return render_template('wine/countriesRegions.html',
                           countries=countries,
                           regions=regions,
                           deletableCountries=deletableCountries,
                           deletableRegions=deletableRegions)


# Create a new country
@app.route('/wine/countryNew', methods=['GET', 'POST'])
def wineCountryNew():
    """Create a new country"""
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'])
        DBSession = open_db_session()
        DBSession.add(newCountry)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wineCountriesRegions'))
    else:
        # this should never happen
        return render_template('wine/countriesRegions.html')


# Create a new region
@app.route('/wine/regionNew', methods=['GET', 'POST'])
def wineRegionNew():
    """Create a new region"""
    DBSession = open_db_session()
    countries = DBSession.query(Country).order_by(asc(Country.name)).all()
    if request.method == 'POST':
        newRegion = Region(
            country_id=request.form['country_id'],
            name=request.form['name'])
        DBSession.add(newRegion)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wineCountriesRegions'))
    else:
        DBSession.close()
        return render_template('wine/countriesRegions.html')


# Add a wine to the database
@app.route('/wine/wineNew', methods=['GET', 'POST'])
def wineNew():
    """Create a new wine"""
    DBSession = open_db_session()
    countries = DBSession.query(Country).order_by(asc(Country.name)).all()
    regions = DBSession.query(Region).order_by(asc(Region.name)).all()
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
        newWine = Wine(
            country_id=fields['country_id'],
            region_id=fields['region_id'],
            appellation=fields['appellation'],
            name=fields['name'],
            year=fields['year'],
            price=fields['price'],
            rating=fields['rating'],
            abv=fields['abv'],
            date_tasted=fields['date_tasted'],
            times_tasted=fields['times_tasted'],
            label_photo=fields['label_photo'],
            purchased_at=fields['purchased_at'],
            description=fields['description'],
            sommelier_id=fields['sommelier_id']
            )
        DBSession.add(newWine)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wineHome'))
    else:
        DBSession.close()
        return render_template('wine/wineNew.html', countries=countries, regions=regions)


# Delete an unassociated (no regions or wines) country
@app.route('/wine/countryDelete', methods=['GET', 'POST'])
def wineCountryDelete():
    """Delete a country"""
    if request.method == 'POST':
        countryID = request.form['country_id']
        DBSession = open_db_session()
        countryToDelete = DBSession.query(Country).filter_by(id=countryID).one_or_none()
        DBSession.delete(countryToDelete)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wineCountriesRegions'))
    else:
        return render_template('wine/countriesRegions.html')


# Delete an unassociated (no wines) region
@app.route('/wine/regionDelete', methods=['GET', 'POST'])
def wineRegionDelete():
    """Delete a region"""
    if request.method == 'POST':
        regionID = request.form['region_id']
        DBSession = open_db_session()
        regionToDelete = DBSession.query(Region).filter_by(id=regionID).one_or_none()
        DBSession.delete(regionToDelete)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wineCountriesRegions'))
    else:
        return render_template('wine/countriesRegions.html')


# Delete a wine from the wine table
@app.route('/wine/wineDelete')
def wineDelete():
    """Delete a wine"""
    # Fetch wine's ID from query_string
    wineid = request.args.get("wineid")
    DBSession = open_db_session()
    wineToDelete = DBSession.query(Wine).filter_by(id=wineid).one_or_none()
    DBSession.delete(wineToDelete)
    DBSession.commit()
    DBSession.close()
    return redirect(url_for('wineTable'))


if __name__ == '__main__':
    app.secret_key = 'sd8f7w4qotgSUF'
    app.debug = True
    app.run()