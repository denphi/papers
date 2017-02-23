
from api.models.user import User
from flask_restful import abort, Resource, fields, marshal_with

address_serializer = {
    'street_number': fields.String,
    'route': fields.String,
    'locality': fields.String,
    'postal_town': fields.String,
    'administrative_area_level_2': fields.String,
    'administrative_area_level_1': fields.String,
    'country': fields.String,
    'postal_code': fields.String
}

user_serializer = {
    'id': fields.String,
    'fullname': fields.String,
    'email': fields.String,
    'address': fields.Nested(address_serializer),
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822')
}

class List(Resource):

    @marshal_with(user_serializer)
    def get(self):
        try:
            return User.get_all()
        except Exception as e:
            abort(400, message="Error getting all users -> {0}".format(e))
