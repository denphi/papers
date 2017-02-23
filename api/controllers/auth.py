from flask_restful import reqparse, abort, Resource

from api.models.user import User
from api.utils.errors import ValidationError

class AuthLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='You need to enter your e-mail address', required=True)
        parser.add_argument('password', type=str, help='You need to enter your password', required=True)

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')

        try:
            token = User.validate(email, password)
            return {'token': token}
        except ValidationError as e:
            abort(400, message="There was an error while trying to log you in -> {0}".format(e))

class AuthRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', type=str, help='You need to enter your full name', required=True)
        parser.add_argument('email', type=str, help='You need to enter your e-mail address', required=True)
        parser.add_argument('password', type=str, help='You need to enter your chosen password', required=True)
        parser.add_argument('password_conf', type=str, help='You need to enter the confirm password field', required=True)

        parser.add_argument('street_number', type=str, help='Address Street Number')
        parser.add_argument('route', type=str, help='Address route')
        parser.add_argument('locality', type=str, help='Address House Name')
        parser.add_argument('postal_town', type=str, help='Address Town')
        parser.add_argument('administrative_area_level_2', type=str, help='Address Area')
        parser.add_argument('administrative_area_level_1', type=str, help='Address Area')
        parser.add_argument('country', type=str, help='Address Country')
        parser.add_argument('postal_code', type=str, help='Address Postal Code')

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')
        password_conf = args.get('password_conf')
        fullname = args.get('fullname')

        street_number = args.get('street_number')
        route = args.get('route')
        locality = args.get('locality')
        postal_town = args.get('postal_town')
        administrative_area_level_2 = args.get('administrative_area_level_2')
        administrative_area_level_1 = args.get('administrative_area_level_1')
        country = args.get('country')
        postal_code = args.get('postal_code')

        try:
            User.create(
                email=email,
                password=password,
                password_conf=password_conf,
                fullname=fullname,

                street_number = street_number,
                route = route,
                locality = locality,
                postal_town = postal_town,
                administrative_area_level_2 = administrative_area_level_2,
                administrative_area_level_1 = administrative_area_level_1,
                country = country,
                postal_code = postal_code
            )
            return {'message': 'Successfully created your account.'}
        except ValidationError as e:
            abort(400, message="There was an error while trying to create your account -> {0}".format(e))
