""" Home page for exultoshores.com """

import os

from flask import (Blueprint,
                   render_template)

home_bp = Blueprint(
    'home_bp', __name__,
    static_folder='static',
    template_folder='templates'
    )

# Display front end for the whole site
@home_bp.route('/')
def showSiteIndex():
    """Display exultoshores.com index page"""
    return render_template('index.html')


# Testing view
@home_bp.route('/testing')
def eosTesting():
    """ Display Test Results """
    envvars = os.environ
    return render_template('testing.html', kwargs=envvars)