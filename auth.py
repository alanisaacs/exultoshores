#!/usr/bin/env python3

"""Handle User Authentication"""

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

# Callback used to reload the user object from the user ID stored in the session
# Returns None if the ID is not valid
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Provide default implementations for the methods that Flask-Login expects user objects to have.
flask_login.UserMixin
# is_authenticated, is_active, is_anonymous, get_id()

@app.route('/login', methods=['GET', 'POST'])
def login():
    # FROM https://flask-login.readthedocs.io/en/latest/:
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user) 
        # or ... flask_login.login_user() -- params include remember, duration, etc

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route("/settings")
@login_required
def settings():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)

# MORE FROM https://flask-login.readthedocs.io/en/latest/
# “Remember Me” functionality  - just pass remember=True to the login_user call. 
# A cookie will be saved on the user’s computer, and then Flask-Login will automatically 
# restore the user ID from that cookie if it is not in the session. The amount of time 
# before the cookie expires can be set with the REMEMBER_COOKIE_DURATION configuration 
# or it can be passed to login_user. 

# FRESH LOGIN REQUIRED (see doc), SESSION_PROTECTION

# flask_login.login_url(login_view, next_url=None, next_field='next')