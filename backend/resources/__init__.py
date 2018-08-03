from flask import request
from http import HTTPStatus
from flask_restful import Resource, reqparse, abort
from utils.error_list import ValidationError
from utils import check_url_params_set, str2bool, DateTimeEncoder
from decorators import login_required, validate_user
from models._models import User, Permissions, TokenBlacklist, jwt, Pages, Chat
from json import dumps, loads


class CreateChat(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='You need to enter your name', required=True)
        parser.add_argument('message', type=str, help='You need to enter your message', required=True)
        status = Chat.create(parser.parse_args())
        return status

        # email = args.get('email')
        # password = args.get('password')
        #
        # try:
        #     token = User.validate(email, password)
        #     return {'token': token}, 200, {'Set-Cookie': 'token={0}; Path=/; Secure; HttpOnly'.format(token)}
        # except ValidationError as e:
        #     abort(400, message='There was an error while trying to log you in -> {}'.format(e))


class ListChats(Resource):
    def get(self):
        chats = Chat.get_all("created")
        return loads(dumps(chats, cls=DateTimeEncoder))


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
            return {'token': token}, 200, {'Set-Cookie': 'token={0}; Path=/; Secure; HttpOnly'.format(token)}
        except ValidationError as e:
            abort(400, message='There was an error while trying to log you in -> {}'.format(e))


class AuthRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('fullname', type=str, help='You need to enter your full name', required=True)
        parser.add_argument('email', type=str, help='You need to enter your e-mail address', required=True)
        parser.add_argument('password', type=str, help='You need to enter your chosen password', required=True)
        parser.add_argument('password_conf', type=str, help='You need to enter the confirm password field',
                            required=True)

        args = parser.parse_args()

        email = args.get('email')
        password = args.get('password')
        password_conf = args.get('password_conf')
        fullname = args.get('fullname')

        try:
            User.create(
                email=email,
                password=password,
                password_conf=password_conf,
                fullname=fullname
            )
            return {'message': 'Successfully created your account.'}
        except ValidationError as e:
            abort(400, message='There was an error while trying to create your account -> {}'.format(e.message))

    def get(self):
        token = request.cookies.get("token")
        print(token)
        payload = jwt.decode(token, "abcd", algorithms=['HS256'])
        return {'jwt': payload}


class TokenBlacklistResource(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='Rate to charge for this resource')
        parser.add_argument('name', type=str, help='Rate to charge for this resource')
        parser.add_argument('category', type=str, help='Rate to charge for this resource')
        parser.add_argument('registry', type=str, help='Rate to charge for this resource')
        self.args = parser.parse_args()

    @login_required
    def get(self):
        filter_dict = {}
        for key, value in self.args.items():
            if value is not None:
                filter_dict[key] = value
        if check_url_params_set(self.args):
            if self.args.get("id") is not None:
                return TokenBlacklist.find(self.args.get("id"))
            else:
                results = TokenBlacklist.filter(filter_dict)
        else:
            results = TokenBlacklist.get_all()
        return results

    def post(self):
        post_args = self.args
        if post_args["id"]:
            del post_args['id']
        TokenBlacklist.create(post_args)
        return {"status": HTTPStatus.CREATED, "message": "Record Created"}, HTTPStatus.CREATED

    def delete(self):
        TokenBlacklist.delete(self.args.get("id"))
        return {"status": HTTPStatus.ACCEPTED, "message": "Record Deleted"}, HTTPStatus.ACCEPTED

    def put(self):
        id = self.args.get("id")
        put_args = self.args
        if put_args["id"]:
            del put_args['id']
        TokenBlacklist.update(id, put_args)
        return {"status": HTTPStatus.ACCEPTED, "message": "Record Updated"}, HTTPStatus.ACCEPTED


class PermissionsResource(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, help='Rate to charge for this resource')
        parser.add_argument('name', type=str, help='Rate to charge for this resource')
        parser.add_argument('number', type=str, help='Rate to charge for this resource')
        self.args = parser.parse_args()

    def get(self):
        filter_dict = {}
        for key, value in self.args.items():
            if value is not None:
                filter_dict[key] = value
        if check_url_params_set(self.args):
            if self.args.get("id") is not None and not self.args.get("relation"):
                return Permissions.find(self.args.get("id"))
            else:
                results = Permissions.filter(filter_dict)
        else:
            results = Permissions.get_all()
        return results

    def post(self):
        post_args = self.args
        if post_args["id"]:
            del post_args['id']
        Permissions.create(post_args)
        return {"status": HTTPStatus.CREATED, "message": "Record Created"}, HTTPStatus.CREATED

    def delete(self):
        Permissions.delete(self.args.get("id"))
        return {"status": HTTPStatus.ACCEPTED, "message": "Record Deleted"}, HTTPStatus.ACCEPTED

    def put(self):
        id = self.args.get("id")
        put_args = self.args
        if put_args["id"]:
            del put_args['id']
        Permissions.update(id, put_args)
        return {"status": HTTPStatus.ACCEPTED, "message": "Record Updated"}, HTTPStatus.ACCEPTED


class UsersResource(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, help='John', required=True)
        parser.add_argument('last_name', type=str, help='Snow', required=True)
        parser.add_argument('email', type=str, help='mail@abcd.com', required=True)
        parser.add_argument('password', type=str, help='some witty password', required=True)
        parser.add_argument('password_conf', type=str, help='some witty password', required=True)
        parser.add_argument('address', type=str, help='your address', default=None)
        parser.add_argument('zip', type=str, help='your zip code', default=None)
        parser.add_argument('phone', type=str, help='phone number', default=None)
        parser.add_argument('mode', type=str, help='the user mode', default='buyer')
        parser.add_argument('ban', type=bool, help='True or False', default=False)
        parser.add_argument('permissions_by_number', help='permission number list', default=[])
        self.args = parser.parse_args()

    def get(self):
        filter_dict = {}
        for key, value in self.args.items():
            if value is not None:
                filter_dict[key] = value
        if check_url_params_set(self.args):
            if self.args.get("id") is not None and not self.args.get("relation"):
                return Permissions.find(self.args.get("id"))
            else:
                results = Permissions.filter(filter_dict)
        else:
            results = Permissions.get_all()
        return results

    def post(self):
        post_args = self.args
        if post_args["id"]:
            del post_args['id']
        Permissions.create(post_args)
        return {"status": HTTPStatus.CREATED, "message": "Record Created"}, HTTPStatus.CREATED

    def delete(self):
        Permissions.delete(self.args.get("id"))
        return {"status": HTTPStatus.ACCEPTED, "message": "Record Deleted"}, HTTPStatus.ACCEPTED

    def put(self):
        id = self.args.get("id")
        put_args = self.args
        if put_args["id"]:
            del put_args['id']
        Permissions.update(id, put_args)
        return {"status": HTTPStatus.ACCEPTED, "message": "Record Updated"}, HTTPStatus.ACCEPTED


class PagesResource(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page_name', type=str, help='home', required=False)
        parser.add_argument('page_data', type=list, location='json', help='Snow', required=False)
        self.args = parser.parse_args()

    def get(self):
        if check_url_params_set(self.args):
            if self.args.get("id") is not None:
                return Pages.find(self.args.get("id"))
            else:
                return {"status": HTTPStatus.NOT_FOUND, "message": "Page not found"}, HTTPStatus.NOT_FOUND
        else:
            results = Pages.filter({'page_name': 'home'})
        return results[0]

    # def post(self):
    #     post_args = self.args
    #     if post_args["id"]:
    #         del post_args['id']
    #     Permissions.create(post_args)
    #     return {"status": HTTPStatus.CREATED, "message": "Record Created"}, HTTPStatus.CREATED

    def delete(self):
        Pages.delete(self.args.get("id"))
        return {"status": HTTPStatus.ACCEPTED, "message": "Page Deleted"}, HTTPStatus.ACCEPTED

    def put(self):
        id = self.args.get("id")
        put_args = self.args
        if put_args["id"]:
            del put_args['id']
        Pages.update(id, put_args)
        return {"status": HTTPStatus.ACCEPTED, "message": "Page Updated"}, HTTPStatus.ACCEPTED
