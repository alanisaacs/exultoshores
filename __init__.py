#!/usr/bin/env python3

"""Initialize Flask application framework for EOS"""

import os
from flask import Flask
from flask_login import LoginManager

from auth.routes import auth_bp
from home import home_bp
from labels.routes import labels_bp
from wine.routes import wine_bp
from models import (open_db_session,
                    Sommelier)


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

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.login_message = 'Access requires logging in'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    DBSession = open_db_session()
    user = DBSession.query(Sommelier).get(int(user_id))
    DBSession.close()
    return user


if __name__ == '__main__':
    app.run()