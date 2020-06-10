import os
import re

import rethinkdb as r
from datetime import datetime

from flask import current_app

from api.models.RethinkDBModel import RethinkDBModel

rdb = r.RethinkDB()
conn = rdb.connect(db=current_app.config['DATABASE_NAME'])
class File(RethinkDBModel):
    _table = 'files'

    @classmethod
    def create(cls, **kwargs):
        name = kwargs.get('name')
        size = kwargs.get('size')
        uri = kwargs.get('uri')
        parent = kwargs.get('parent')
        creator = kwargs.get('creator')
        siteName = kwargs.get('siteName')
        url = kwargs.get('url')

        # Direct parent ID
        parent_id = '0' if parent is None else parent['id']

        doc = {
            'name': name,
            'size': size,
            'uri': uri,
            'siteName': siteName,
            'url': url,            
            'parent_id': parent_id,
            'creator': creator,
            'is_folder': False,
            'status': True,
            'date_created': datetime.now(rdb.make_timezone('+01:00')),
            'date_modified': datetime.now(rdb.make_timezone('+01:00'))
        }

        res = rdb.table(cls._table).insert(doc).run(conn)
        doc['id'] = res['generated_keys'][0]

        if parent is not None:
            Folder.add_object(parent, doc['id'])

        return doc

    @classmethod
    def find(cls, id, listing=False):
        file_ref = rdb.table(cls._table).get(id).run(conn)
        if file_ref is not None:
            if file_ref['is_folder'] and listing and file_ref['objects'] is not None:
                file_ref['objects'] = list(rdb.table(cls._table).get_all(r.args(file_ref['objects'])).run(conn))
        return file_ref

    @classmethod
    def move(cls, obj, to):
        previous_folder_id = obj['parent_id']
        previous_folder = Folder.find(previous_folder_id)
        Folder.remove_object(previous_folder, obj['id'])
        Folder.add_object(to, obj['id'])
