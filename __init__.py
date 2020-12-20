#!/usr/bin/env python3

"""Initialize Flask application framework for EOS"""

import os
from flask import Flask

from auth.routes import auth_bp
from home import home_bp
from labels.routes import labels_bp
from wine.routes import wine_bp


# Create Flask app
app = Flask(__name__)


# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(labels_bp)
app.register_blueprint(wine_bp)

# Set Flask app configs from environment variables
app.env = os.environ.get('FLASK_ENV')
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

if __name__ == '__main__':
    app.run()