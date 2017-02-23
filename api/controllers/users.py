
from api.models import User
from flask_restful import abort, Resource, fields, marshal_with

user_serializer = {
    'fullname': fields.String,
    'email': fields.String,
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822')
}

class List(Resource):

    @marshal_with(user_serializer)
    def get(self):
        try:
            return User.get_all()
        except:
            abort(400, message="Error getting all users -> {}".format(e.message))
