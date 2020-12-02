#!/usr/bin/env python3

"""Initialize Flask application framework for EOS"""

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


if __name__ == '__main__':
    app.secret_key = 'sd8f7w4qotgSUF'
    app.debug = True
    app.run()