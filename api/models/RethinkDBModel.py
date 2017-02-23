import os
import re

import rethinkdb as r

from flask import current_app

from api.utils.errors import ValidationError, DatabaseProcessError, UnavailableContentError

conn = r.connect(db='papers')

class RethinkDBModel(object):

    @classmethod
    def find(cls, id):
        return r.table(cls._table).get(id).run(conn)

    @classmethod
    def filter(cls, predicate):
        return list(r.table(cls._table).filter(predicate).run(conn))

    @classmethod
    def update(cls, id, fields):
        status = r.table(cls._table).get(id).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    def delete(cls, id):
        status = r.table(cls._table).get(id).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True

    @classmethod
    def update_where(cls, predicate, fields):
        status = r.table(cls._table).filter(predicate).update(fields).run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the update action")
        return True

    @classmethod
    def delete_where(cls, predicate):
        status = r.table(cls._table).filter(predicate).delete().run(conn)
        if status['errors']:
            raise DatabaseProcessError("Could not complete the delete action")
        return True
