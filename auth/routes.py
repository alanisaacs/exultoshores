import hashlib
import uuid
from flask import (Blueprint,
                   flash,
                   redirect,
                   render_template,
                   request,
                   session as login_session,
                   url_for)

from models import (open_db_session,
                    Sommelier)


auth_bp = Blueprint(
    'auth_bp', __name__,
    static_folder='static',
    static_url_path='/auth/static',
    template_folder='templates'
    )

# Log In Existing User
@auth_bp.route('/wine/login', methods=['GET', 'POST'])
def wineLogin():
    """Log in as existing user"""
    # Simplest flow
    # Validate submission
    if request.method == 'POST':
        # get Sommelier associated with user in db
        DBSession = open_db_session()
        som = DBSession.query(Sommelier).filter_by(username = request.form['username']).one_or_none()
        DBSession.close()
        # confirm password matches hashed version
        pwMatch = check_password(som.password, request.form['password'])
        if pwMatch:
            login_session['username'] = request.form['username']
            flash("===LOGIN SUCCESSFUL===", "messageSuccess")
            return render_template('/login.html')
        else:
            flash("===LOGIN FAILED! PLEASE TRY AGAIN===", "messageError")
            return render_template('login.html')
    # Display form
    else:
        return render_template('/login.html')

# Log out user
@auth_bp.route('/wine/logout')
def wineLogout():
    """ Remove the username from the session if it's there """
    login_session.pop('username', None)
    return redirect(url_for('wineHome'))

# Create new user
@auth_bp.route('/wine/wineNewUser', methods=['POST'])
def wineNewUser():
    """ Create new user with hashed password in db """
    if request.method == 'POST':
        # hash password with salt
        hashed_pw = hash_password(request.form['password'])
        # create new user in database
        newuser = Sommelier(
            username = request.form['username'],
            password = hashed_pw,
            email = request.form['email'],
            picture = request.form['picture']
        )
        DBSession = open_db_session()
        DBSession.add(newuser)
        DBSession.commit()
        DBSession.close()
        login_session['username'] = request.form['username']
        flash("===ACCOUNT SUCCESSFULLY CREATED===", "messageSuccess")
        return render_template('/login.html')
    else:
        return render_template('/error.html')


def hash_password(password):
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
 
