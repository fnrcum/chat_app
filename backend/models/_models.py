from . import *


class TokenBlacklist(RethinkDBModel):
    _table = 'token_blacklist'
    _pk = "id"

    @classmethod
    def create(cls, args):
        post_args = args
        del post_args['id']
        if not ("name") in post_args:
            return {"status": HTTPStatus.BAD_REQUEST,
                    "message": "Invalid request params, Accepted: 'name'"}, HTTPStatus.BAD_REQUEST
        for key, value in post_args.items():
            if value is None or value is "":
                return {"status": HTTPStatus.BAD_REQUEST,
                        "message": "Invalid request params: {0} has no value}".format(key)}, HTTPStatus.BAD_REQUEST
        with pool.get_resource() as res:
            r.table(cls._table).insert(post_args).run(res.conn)


class Permissions(RethinkDBModel):
    _table = 'permissions'
    _pk = 'id'

    @classmethod
    def create(cls, args):
        post_args = args
        if not ("name" and "id") in post_args:
            return {"status": HTTPStatus.BAD_REQUEST,
                    "message": "Invalid request params, Accepted: 'name', 'id'"}, HTTPStatus.BAD_REQUEST
        for key, value in post_args.items():
            if value is None or value is "":
                return {"status": HTTPStatus.BAD_REQUEST,
                        "message": "Invalid request params: {0} has no value}".format(key)}, HTTPStatus.BAD_REQUEST
        with pool.get_resource() as res:
            r.table(cls._table).insert(post_args).run(res.conn)


class User(RethinkDBModel):
    _table = 'users'
    _pk = 'id'

    @classmethod
    def create(cls, **kwargs):
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password_conf = kwargs.get('password_conf')
        address = kwargs.get('address')
        zip = kwargs.get('zip')
        phone = kwargs.get('phone')
        token = None or kwargs.get('token')
        mode = None or kwargs.get('mode')
        ban = None or kwargs.get('ban')
        permissions_by_name = None or kwargs.get('permissions_by_name')
        if password != password_conf:
            raise ValidationError("Password and Confirm password need to be the same value")
        doc = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': cls.hash_password(password),
            'address': address,
            'zip': zip,
            'phone': phone,
            'token': token,
            'permissions_by_id': permissions_by_name,
            'mode': mode,
            'ban': ban,
            'date_created': datetime.now(r.make_timezone('+02:00')),
            'date_modified': datetime.now(r.make_timezone('+02:00'))
        }
        with pool.get_resource() as res:
            r.table(cls._table).insert(doc).run(res.conn)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)

    @classmethod
    def validate(cls, email, password):
        with pool.get_resource() as res:
            docs = list(r.table(cls._table).filter({'email': email}).run(res.conn))

        if not len(docs):
            raise ValidationError("Could not find the e-mail address you specified")

        _hash = docs[0]['password']

        if cls.verify_password(password, _hash):
            try:
                payload = {'id': docs[0]['id'],
                           'date_time': (datetime.now() + timedelta(days=0, hours=0, minutes=5)).strftime("%Y-%m-%d %H:%M:%S")}
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except JWTError:
                raise ValidationError("There was a problem while trying to create a JWT token.")
        else:
            raise ValidationError("The password you inputted was incorrect.")


class Pages(RethinkDBModel):
    _table = 'pages'
    _pk = 'id'

    @classmethod
    def create(cls, **kwargs):
        page_name = kwargs.get('page_name')
        page_data = kwargs.get('page_data')
        doc = {
            'page_name': page_name,
            'page_data': page_data,
            'date_created': datetime.now(r.make_timezone('+02:00')),
            'date_modified': datetime.now(r.make_timezone('+02:00'))
        }
        with pool.get_resource() as res:
            r.table(cls._table).insert(doc).run(res.conn)

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)

    @staticmethod
    def verify_password(password, _hash):
        return pbkdf2_sha256.verify(password, _hash)

    @classmethod
    def validate(cls, email, password):
        with pool.get_resource() as res:
            docs = list(r.table(cls._table).filter({'email': email}).run(res.conn))

        if not len(docs):
            raise ValidationError("Could not find the e-mail address you specified")

        _hash = docs[0]['password']

        if cls.verify_password(password, _hash):
            try:
                payload = {'id': docs[0]['id'],
                           'date_time': (datetime.now() + timedelta(days=0, hours=0, minutes=5)).strftime("%Y-%m-%d %H:%M:%S")}
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
                return token
            except JWTError:
                raise ValidationError("There was a problem while trying to create a JWT token.")
        else:
            raise ValidationError("The password you inputted was incorrect.")


class Chat(RethinkDBModel):
    _table = 'chats'
    _pk = "id"

    @classmethod
    def create(cls, args):
        data = args
        data['created'] = datetime.now(r.make_timezone('00:00'))
        with pool.get_resource() as res:
            if data.get('name') and data.get('message'):
                r.table("chats").insert([data]).run(res.conn)
                return {"status": HTTPStatus.CREATED, "message": "Successfully Created}"}, HTTPStatus.CREATED
            return {"status": HTTPStatus.BAD_REQUEST, "message": "Invalid Chat Supplied}"}, HTTPStatus.BAD_REQUEST