
from flask import Blueprint #flask's Blueprint class that is used to
#group similar code or views(routes)(modularity)

from flask import request #flask's object representing http request itself
#it alows for example checking which request method was used or what was
#POST'ed in form

bp = Blueprint('auth',__name__,url_prefix='/auth') #create a Blueprint
# that is named auth, takes __name__ argument(as always), and adds /auth
#to every route created in this Blueprint. this bluprint will be
#added to app factory using app.register_blueprint(auth.bp)

from flaskr.db import get_db #our self made function returning connection to
#sqlite databases

from werkzeug.security import generate_password_hash# function used to
#store passwords in database as hashes, not in plain text

from flask import redirect, url_for# redirect makes you go to different
#url while not changing url that is written in browser window
#url_for gives you route for the the view(route function) you give it

from flask import render_template#makes it possible to return html site

from flask import flash #makes it possible to show simple massages to user
#directly from app (with no additional html files)

@bp.route('/register',methods = ['GET','POST']) # auth/register url accept methods
# get and post. post is correct, secure solution so we handle it, get makes us
#reload the registration page

def register(): #view function register

    if request.method == 'POST':
        username = request.form['username'] #get value from form filled be user
        # with id/name (not sure which one it was) username and assign for later

        password = request.form['password']
        db = get_db() #create connection to database

        error = None #give error variable default value

    if not username:      #set error depending on what user filled in form
        error = "Username is required"
    elif not password:
        error = "Password is required"
    elif db.execute( #direct sql query using sqlite3 methods
        'SELECT id FROM user WHERE username = ?',(username,)
    ).fetchone() is not None:
        error = "User {} is already registered".format(username)

    if error is None: #when no error, insert new user into database
        db.execute(
            'INSERT INTO user (username, password) VALUES (?, ?)',
            (username, generate_password_hash(password)) #password stored as hash
        )
        db.commit() # if data is modified, not read only, we need to commit changes

        return redirect(url_for('auth.login')) # if registration succesfull,
        #redirect to url responsible for login view function. 'auth.' before
        #login is necessary because this view function is part of blueprint

    flash(error) #renders error message to user

return render_template('auth/register.html') #gets returned if registration went
#wrong (any of 3 errors happened)
