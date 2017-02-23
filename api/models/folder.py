import os
import re

import rethinkdb as r
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime
from passlib.hash import pbkdf2_sha256

from flask import current_app

from api.models.RethinkDBModel import RethinkDBModel
from api.models.file import File

conn = r.connect(db='papers')

class Folder(File):
    @classmethod
    def create(cls, **kwargs):
        name = kwargs.get('name')
        parent = kwargs.get('parent')
        creator = kwargs.get('creator')

        # Direct parent ID
        parent_id = '0' if parent is None else parent['id']

        doc = {
            'name': name,
            'parent_id': parent_id,
            'creator': creator,
            'is_folder': True,
            'last_index': 0,
            'status': True,
            'objects': None,
            'date_created': datetime.now(r.make_timezone('+01:00')),
            'date_modified': datetime.now(r.make_timezone('+01:00'))
        }

        res = r.table(cls._table).insert(doc).run(conn)
        doc['id'] = res['generated_keys'][0]

        if parent is not None:
            cls.add_object(parent, doc['id'], True)

        cls.tag_folder(parent, doc['id'])

        return doc

    @classmethod
    def move(cls, obj, to):
        if to is not None:
            parent_tag = to['tag']
            child_tag = obj['tag']

            parent_sections = parent_tag.split("#")
            child_sections = child_tag.split("#")

            if len(parent_sections) > len(child_sections):
                matches = re.match(child_tag, parent_tag)
                if matches is not None:
                    raise Exception("You can't move this object to the specified folder")

        previous_folder_id = obj['parent_id']
        previous_folder = cls.find(previous_folder_id)
        cls.remove_object(previous_folder, obj['id'])

        if to is not None:
            cls.add_object(to, obj['id'], True)

    @classmethod
    def remove_object(cls, folder, object_id):
        update_fields = folder['objects'] or []
        while object_id in update_fields:
            update_fields.remove(object_id)
        cls.update(folder['id'], {'objects': update_fields})

    @classmethod
    def add_object(cls, folder, object_id, is_folder=False):
        p = {}
        update_fields = folder['objects'] or []
        update_fields.append(object_id)

        if is_folder:
            p['last_index'] = folder['last_index'] + 1

        p['objects'] = update_fields
        cls.update(folder['id'], p)

    @classmethod
    def tag_folder(cls, parent, id):
        tag = id if parent is None else "{0}#{1}".format(parent['tag'], parent['last_index'])
        cls.update(id, {'tag': tag})
