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
    if os.getenv('EOS_TEST_MODE') == 'True':
        envvars = os.environ
        sorted_envvars_keys = sorted(os.environ)
        from __init__ import app
        flask_configs = app.config
        return render_template('testing.html', 
            envvars=envvars, sorted_envvars_keys=sorted_envvars_keys,
            flask_configs=flask_configs)
    else:
        return "Testing not enabled"


# Display About page
@home_bp.route('/about')
def showAbout():
    """Display About page"""
    return render_template('about.html')
