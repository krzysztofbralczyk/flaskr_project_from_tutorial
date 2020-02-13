import sqlite3 #import module for connecting python with database
import click #import module in which command line interface is written
from flask import g #import object that is used to pass around data
#during single request
from flask import current_app # similar to 'g', current_app points to the app
#that is handling current request, thanks to it you don't need to pass around
#app instance, just 'pointer' to it. It is also necessary when you want to
#reference app instance when it doesn't exist like right now. We are creating
#app factory so app instance doesn't exist yet, but we need to reference it to
#set up connection with database

#both g and current_app are part of application context in flask and are to
#complicated for me right now, need more examples and experience, so far I
#understand that they are used to pass data during requests and when using CLI
#and that they can't be used to pass data between requests (use session).
#g is also used to pass data between different functions during single request
# for example database connection to sqlite may be passes and reused by functions

from flask.cli import with_appcontext #can't find any explanation

#this whole function basically returns database connection
def get_db(): #function creating db connection
    if 'db' not in g: # if g doesn't have db attribute
        g.db = sqlite3.connect( #create g.db attribute and assing database
        #connection to it
            current_app.config['DATABASE'], #database config, first argument is
            #necessary and is a string with path to database file
            detect_types=sqlite3.PARSE_DECLTYPES # NO IDEA
        )
        g.db.row_factory = sqlite3.Row # not sure, sqlite3.Row is a Class which
        #instances are objects representing single row in a table. They are
        #usefull because with them we can for example access columns by names,
        #not by indices. row_factory will be db atribute that will be used to
        #create such objects(rows)

    return g.db #function returns database connection which is passed around
    #functions in the same request as attribute of g

def close_db(e=None): #function to close database connection, it will be used
#after each request
    db = g.pop('db',None) #get and delete 'db' attribute from g objects
    if db is not None:
        db.close() #if g.pop did not return None (database connection exists),
        #then close database connection
