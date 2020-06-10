import os
import re

import rethinkdb as r
import jwt
from jwt.exceptions import PyJWTError as JWTError 

from datetime import datetime
from passlib.hash import pbkdf2_sha256

from flask import current_app
from api.utils.errors import ValidationError, DatabaseProcessError, UnavailableContentError
from api.models.RethinkDBModel import RethinkDBModel

rdb = r.RethinkDB()
conn = rdb.connect(db=current_app.config['DATABASE_NAME'])

class User(RethinkDBModel):
    _table = 'users'

    @classmethod
    def create(cls, **kwargs):
        fullname = kwargs.get('fullname')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password_conf = kwargs.get('password_conf')

        street_number = kwargs.get('street_number')
        route = kwargs.get('route')
        locality = kwargs.get('locality')
        postal_town = kwargs.get('postal_town')
        administrative_area_level_2 = kwargs.get('administrative_area_level_2')
        administrative_area_level_1 = kwargs.get('administrative_area_level_1')
        country = kwargs.get('country')
        postal_code = kwargs.get('postal_code')

        if password != password_conf:
            raise ValidationError("Password and Confirm password need to be the same value")
        password = cls.hash_password(password)
        doc = {
            'fullname': fullname,
            'email': email,
            'password': password,
            'address': {
                'street_number': street_number,
                'route': route,
                'locality': locality,
                'postal_town': postal_town,
                'administrative_area_level_2': administrative_area_level_2,
                'administrative_area_level_1': administrative_area_level_1,
                'country': country,
                'postal_code': postal_code
            },
            'date_created': datetime.now(rdb.make_timezone('+01:00')),
            'date_modified': datetime.now(rdb.make_timezone('+01:00')),
        }

        print(doc)

        users = list(rdb.table(cls._table).filter({'email': email}).run(conn))
        if len(users):
            raise ValidationError("Could already exists with e-mail address: {0}".format(email))

        rdb.table(cls._table).insert(doc).run(conn)

    @classmethod
    def validate(cls, email, password):
        docs = list(rdb.table(cls._table).filter({'email': email}).run(conn))

        if not len(docs):
            raise ValidationError("Could not find the e-mail address you specified")

        _hash = docs[0]['password']

        if cls.verify_password(password, _hash):
            try:
                token = jwt.encode({'id': docs[0]['id']}, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except JWTError:
                raise ValidationError("There was a problem while trying to create a JWT token.")
        else:
            raise ValidationError("The password you inputed was incorrect.")

    @classmethod
    def get_all(cls):
        return list(rdb.table(cls._table).run(conn))

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)
