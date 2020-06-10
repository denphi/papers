import os
import re

import rethinkdb as r

from flask import current_app

from api.utils.errors import ValidationError, DatabaseProcessError, UnavailableContentError

rdb = r.RethinkDB()
conn = rdb.connect(db='papers')

class RethinkDBModel(object):

    @classmethod
    def find(cls, id):
        return rdb.table(cls._table).get(id).run(conn)

    @classmethod
    def filter(cls, predicate):
        return list(rdb.table(cls._table).filter(predicate).run(conn))

    @classmethod
    def update(cls, id, fields):
        status = rdb.table(cls._table).get(id).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    def delete(cls, id):
        status = rdb.table(cls._table).get(id).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True

    @classmethod
    def update_where(cls, predicate, fields):
        status = rdb.table(cls._table).filter(predicate).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    def delete_where(cls, predicate):
        status = rdb.table(cls._table).filter(predicate).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True
