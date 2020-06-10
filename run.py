import inspect
import importlib
from rethinkdb import r

from flask_script import Manager

from api import create_app

app = create_app('development')

manager = Manager(app)

@manager.command
def migrate():
    '''
    Creates Database
    '''
    try:
        db_name = app.config['DATABASE_NAME']
        conn = r.connect()

        # Create Tables
        if db_name not in r.db_list().run(conn):
            db = r.db_create(db_name).run(conn)
            print("Created database '{0}'...".format(db_name))

        # Create the application tables if they do not exist
        lib = importlib.import_module('api.models')
        for cls in inspect.getmembers(lib, inspect.isclass):
            for base in cls[1].__bases__:
                if base.__name__ == "RethinkDBModel":
                    table_name = getattr(cls[1], '_table')
                    r.db(db_name).table_create(table_name).run(conn)
                    print("Created table '{0}'...".format(table_name))
        print("Running RethinkDB migration command")
    except Exception as e:
        print("An error occured --> {0}".format(e))

@manager.command
def drop_db():
    '''
    Drops Database
    '''
    try:
        db_name = app.config['DATABASE_NAME']
        conn = r.connect()
        if db_name in r.db_list().run(conn):
            r.db_drop(db_name).run(conn)
    except Exception as e:
        print("An error occured --> {0}".format(e))

if __name__ == '__main__':
    manager.run()
