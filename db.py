import sqlite3  # import module for connecting python with database
import click  # import module in which command line interface is written
from flask import g  # import object that is used to pass around data
# during single request
from flask import current_app  # similar to 'g', current_app points to the app
# that is handling current request, thanks to it you don't need to pass around
# app instance, just 'pointer' to it. It is also necessary when you want to
# reference app instance when it doesn't exist like right now. We are creating
# app factory so app instance doesn't exist yet, but we need to reference it to
# set up connection with database

# both g and current_app are part of application context in flask and are to
# complicated for me right now, need more examples and experience, so far I
# understand that they are used to pass data during requests and when using CLI
# and that they can't be used to pass data between requests (use session).
# g is also used to pass data between different functions during single request
# for example database connection to sqlite may be passes and reused by functions

from flask.cli import with_appcontext  # can't find any explanation


# this whole function basically returns database connection
def get_db():  # function creating db connection
    if 'db' not in g:  # if g doesn't have db attribute
        g.db = sqlite3.connect(  # create g.db attribute and assign database
            # connection to it
            current_app.config['DATABASE'],  # database config, first argument is
            # necessary and is a string with path to database file
            detect_types=sqlite3.PARSE_DECLTYPES  # NO IDEA
        )
        g.db.row_factory = sqlite3.Row  # not sure, sqlite3.Row is a Class which
        # instances are objects representing single row in a table. They are
        # useful because with them we can for example access columns by names,
        # not by indices. row_factory will be db method that will be used to
        # create such objects(rows)

    return g.db  # function returns database connection which is passed around
    # functions in the same request as attribute of g


def close_db(e=None):  # function to close database connection, it will be used
    # after each request                                                                WHAT IS e=
    db = g.pop('db', None)  # get and delete 'db' attribute from g objects           NONE?
    if db is not None:
        db.close()  # if g.pop did not return None (database connection exists),
        # then close database connection


def init_db():  # code to create database by running sql script in schema.sql
    db = get_db()  # db will be our connection to database

    with current_app.open_resource('schema.sql') as f:  # open_resource is
        # flask's version of open() that opens file in path relative to application
        # root folder and additionally don't allow write mode that would be bad to
        # use for app in production
        db.executescript(f.read().decode('utf8'))  # executescript is sqlite3
        # module command that is used to do direct SQL queries in short way (there is
        # more official, longer way). schema.sql is open with open_resource command.
        # Then it's read() using normal python command which returns single string.
        # then it's decoded from utf8 to 'normal python string'                   ?????


@click.command('init-db')  # using click module, create command line
# command called init-db
@with_appcontext  # makes it possible for function below to have access to context
# of the application, which is not normally included considering it's Click
# decorator and not Flask app's decorator
def init_db_command():
    init_db()
    click.echo("Cleared existing databases. Initialized new database.")  # click
    # command printing string in command line


def init_app(app):  # so far our app knows nothing about functions in this module.
    # Since our app instance doesn't even exist when writing code ('cause we are using
    # application factory) then we can't go to it and config it. That is why we are
    # creating a function init_app() that takes app itself as argument and
    # adds(registers) our functions to it. It will be called by app factory
    # itself (__init__.py) when app is up and running
    app.teardown_appcontext(close_db)  # teardown_appcontext tells flask what to
    # call after returning the response. So after flask app takes a request, it
    # will respond and then call close_db function, closing connection to database
    app.cli.add_command(init_db_command)  # create command line command that can
    # be called with 'flask ...' just like 'flask run'
