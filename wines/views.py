#!/usr/bin/env python3

"""Create web views for the Wine App"""

import sys
from flask import (Flask,
                   render_template,
                   session as login_session)
from sqlalchemy import (create_engine,
                        asc)
from sqlalchemy.orm import sessionmaker
from models import (Base,
                    User,
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
@app.route("/")
def showHome():
    """Display home page"""
    session = DBSession()
    countries = session.query(Country).order_by(asc(Country.name))
    regions = session.query(Region).order_by(asc(Region.name))
    users = session.query(User).order_by(asc(User.username))
    wines = session.query(Wine)
    session.close()
    return render_template('home.html',
                           countries=countries,
                           regions=regions,
                           users=users,
                           wines=wines)


if __name__ == '__main__':
    app.run()