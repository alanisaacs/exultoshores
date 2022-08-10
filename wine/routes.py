"""Create web views for EOS Wine Log"""

from itertools import count
import sys

from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   request,
                   session as login_session,
                   url_for)
from flask_login import login_required
from sqlalchemy import (asc,
                        cast,
                        desc,
                        func,
                        null,
                        Numeric,
                        update)

from models import (Base,
                    Country,
                    open_db_session,
                    Region,
                    Sommelier,
                    Wine)


wine_bp = Blueprint(
    'wine_bp', __name__,
    static_folder='static',
    static_url_path='/wine/static',
    template_folder='templates'
    )


# Display Wine App home page, showing all the wines in the db
@wine_bp.route('/wine')
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
    return render_template('home.html', wines=wines)


# Display a table of all wines
@wine_bp.route('/wine/table')
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
    # Pass number of wines to the template for display
    numWines = len(wines)
    return render_template('table.html', wines=wines, numWines=numWines)


@wine_bp.route('/wine/stats')
def wineStats():
    """Show statistics on the wines in the database"""
    DBSession = open_db_session()
    #### QUERY FOR STATS BY COUNTRY ####
    # Country Table creates object with four columns:
    # name, number of wines, average rating, average price, average abv
    # Note rating and abv are type "real" which has to be cast 
    # as Numeric for the round function to work
    # IN SQL:
    # SELECT 
    #     country.name, 
    #     COUNT(wine.country_id),
	#     ROUND(AVG(wine.rating),2) AS rating, 
	#     ROUND(AVG(wine.price::NUMERIC), 2) AS price, 
	#     ROUND(AVG(wine.ABV::NUMERIC), 2) as abv 
	# FROM wine 
    # JOIN country ON wine.country_id=country.id 
    # GROUP BY country.name 
    # ORDER BY name DESC; 
    wines_by_country = DBSession.query(
                        Country.name, func.count(Wine.country_id),\
                            func.round(func.avg(Wine.rating), 1),\
                            func.round(cast(
                                func.avg(Wine.price), Numeric), 2),\
                            func.round(cast(
                                func.avg(Wine.abv), Numeric), 1)).\
                        join(Wine, Wine.country_id==Country.id).\
                        group_by(Country.name).\
                        order_by(desc(func.count(Wine.country_id)),\
                            Country.name).\
                        all()
    wines_by_region = DBSession.query(
                        Region.name, func.count(Wine.region_id)).\
                        join(Wine, Wine.region_id==Region.id).\
                        group_by(Region.name).\
                        order_by(desc(func.count(Wine.region_id)),\
                            Region.name).\
                        all()
    wines_by_appellation = DBSession.query(
                        Wine.appellation, func.count(Wine.appellation)).\
                        group_by(Wine.appellation).\
                        order_by(desc(func.count(Wine.appellation)),\
                            Wine.appellation).\
                        all()
    wines_by_category = DBSession.query(
                        Wine.categories, func.count(Wine.categories)).\
                        group_by(Wine.categories).\
                        order_by(desc(func.count(Wine.categories)),\
                            Wine.categories).\
                        all()
    wines_by_rating = DBSession.query(
                        Wine.rating, func.count(Wine.rating)).\
                        group_by(Wine.rating).\
                        order_by(desc(Wine.rating)).\
                        all()
    wines_by_abv = DBSession.query(
                        Wine.abv, func.count(Wine.abv)).\
                        group_by(Wine.abv).\
                        order_by(Wine.abv).\
                        all()
    wines_by_year = DBSession.query(
                        Wine.year, func.count(Wine.year)).\
                        group_by(Wine.year).\
                        order_by(Wine.year).\
                        all()
    wines_by_varietals = DBSession.query(
                        Wine.varietals, func.count(Wine.varietals)).\
                        group_by(Wine.varietals).\
                        order_by(desc(func.count(Wine.varietals)),\
                            Wine.varietals).\
                        all()
    total_num_wines = DBSession.query(
                        Wine.year).count()
    DBSession.close()
    return render_template('stats.html',\
        wines_by_country=wines_by_country,\
        wines_by_region=wines_by_region,\
        wines_by_appellation=wines_by_appellation,\
        wines_by_category=wines_by_category,\
        wines_by_rating=wines_by_rating,\
        wines_by_abv=wines_by_abv,\
        wines_by_year=wines_by_year,\
        wines_by_varietals=wines_by_varietals,\
        total_num_wines=total_num_wines)
    
    
# Display a single wine for editing
@wine_bp.route('/wine/wineEdit')
@login_required
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
    # Make some tweaks to the data
    for w in wineDict.copy():
    # display any None (null) values as blank spaces
    # then it is easy to convert them to NULL again
    # on their way back to the database
    # (see newwine view)
        if wineDict[w] == None:
            wineDict[w] = ""
    # remove ids (wine id, country_id, region_id, sommelier_id)
    # use a copy as a dict cannot be changed during iteration
        if w.find('id') != -1:
            wineDict.pop(w)
    # Sort by key (requires building new dictionary)
    sorted_dict = {}
    sorted_keys = sorted(wineDict)
    for k in sorted_keys:
        sorted_dict[k]=wineDict[k]
    return render_template('wineEdit.html', wineid=wineid,
        wineToEdit=sorted_dict, wineDescription=wineDescription)


# Update wine record with values from wineEdit form view
@wine_bp.route('/wine/wineUpdate', methods=['POST'])
@login_required
def wineUpdate():
    """Update a wine record"""
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
    wineid = request.args.get('wineid')
    wineToUpdate = DBSession.query(Wine).\
        filter(Wine.id==wineid)
    # update everything in the form
    # TODO: only update changed items
    for i in fields:
        wineToUpdate.update({
            i: fields[i]
        })
    DBSession.commit()
    DBSession.close()
    return redirect(url_for('wine_bp.wineHome', _anchor=wineid))


# Show counties and regions with create, edit and delete links
@wine_bp.route('/wine/countriesRegions', methods=['GET', 'POST'])
@login_required
def wineCountriesRegions():
    """Manage countries and regions"""
    DBSession = open_db_session()
    countries = DBSession.query(Country).\
        order_by(asc(Country.name)).all()
    regions = DBSession.query(Region).\
        order_by(asc(Region.name)).all()
    deletableCountries = DBSession.query(Country).join(Region, 
        full = True).filter(Region.country_id == None).all()
    deletableRegions = DBSession.query(Region).join(Wine,
        full = True).filter(Wine.region_id == None).all()
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'])
        DBSession.add(newCountry)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        DBSession.close()
        return render_template('countriesRegions.html',
                           countries=countries,
                           regions=regions,
                           deletableCountries=deletableCountries,
                           deletableRegions=deletableRegions)


# Create a new country
@wine_bp.route('/wine/countryNew', methods=['GET', 'POST'])
@login_required
def wineCountryNew():
    """Create a new country"""
    if request.method == 'POST':
        newCountry = Country(name=request.form['name'])
        DBSession = open_db_session()
        DBSession.add(newCountry)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        # Route should only be called with POST
        return redirect(url_for("auth_bp.wineLogin"))


# Create a new region
@wine_bp.route('/wine/regionNew', methods=['GET', 'POST'])
@login_required
def wineRegionNew():
    """Create a new region"""
    DBSession = open_db_session()
    countries = DBSession.query(Country).\
        order_by(asc(Country.name)).all()
    if request.method == 'POST':
        newRegion = Region(
            country_id=request.form['country_id'],
            name=request.form['name'])
        DBSession.add(newRegion)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        DBSession.close()
        return render_template('countriesRegions.html')


# Rename a country
@wine_bp.route('/wine/countryRename', methods=['GET', 'POST'])
@login_required
def wineCountryRename():
    """Rename a country"""
    if request.method == 'POST':
        countryID = request.form['country_id']
        DBSession = open_db_session()
        DBSession.query(Country).\
            filter_by(id=countryID).\
            update({'name': request.form['newname']})
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        return render_template('countriesRegions.html')


# Rename a region
@wine_bp.route('/wine/regionRename', methods=['GET', 'POST'])
@login_required
def wineRegionRename():
    """Rename a region"""
    if request.method == 'POST':
        regionID = request.form['region_id']
        DBSession = open_db_session()
        DBSession.query(Region).\
            filter_by(id=regionID).\
            update({'name': request.form['newname']})
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        return render_template('countriesRegions.html')
        

# Add a wine to the database
@wine_bp.route('/wine/wineNew', methods=['GET', 'POST'])
@login_required
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
            sommelier_id=fields['sommelier_id'],
            categories=fields['categories'],
            varietals=fields['varietals']
            )
        DBSession.add(newWine)
        # Get the id of the new wine just created
        # So it can be passed to home page as anchor
        wineid = DBSession.query(func.max(Wine.id)).scalar()
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineHome', _anchor=wineid))
    else:
        DBSession.close()
        return render_template('wineNew.html', countries=countries, regions=regions)


# Delete an unassociated (no regions or wines) country
@wine_bp.route('/wine/countryDelete', methods=['GET', 'POST'])
@login_required
def wineCountryDelete():
    """Delete a country"""
    if request.method == 'POST':
        countryID = request.form['country_id']
        DBSession = open_db_session()
        countryToDelete = DBSession.query(Country).filter_by(id=countryID).one_or_none()
        DBSession.delete(countryToDelete)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        return render_template('countriesRegions.html')


# Delete an unassociated (no wines) region
@wine_bp.route('/wine/regionDelete', methods=['GET', 'POST'])
@login_required
def wineRegionDelete():
    """Delete a region"""
    if request.method == 'POST':
        regionID = request.form['region_id']
        DBSession = open_db_session()
        regionToDelete = DBSession.query(Region).filter_by(id=regionID).one_or_none()
        DBSession.delete(regionToDelete)
        DBSession.commit()
        DBSession.close()
        return redirect(url_for('wine_bp.wineCountriesRegions'))
    else:
        return render_template('countriesRegions.html')


# Delete a wine from the wine table
@wine_bp.route('/wine/wineDelete')
@login_required
def wineDelete():
    """Delete a wine"""
    # Fetch wine's ID from query_string
    wineid = request.args.get("wineid")
    DBSession = open_db_session()
    wineToDelete = DBSession.query(Wine).filter_by(id=wineid).one_or_none()
    DBSession.delete(wineToDelete)
    DBSession.commit()
    DBSession.close()
    return redirect(url_for('wine_bp.wineTable'))
