from db import *
from http import HTTPStatus
from utils.error_list import *
from datetime import datetime, timedelta
from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from flask import current_app


class RethinkDBModel(object):

    @classmethod
    def get_all(cls, index=None):
        with pool.get_resource() as res:
            if index is None:
                return list(r.table(cls._table).run(res.conn))
            else:
                return list(r.table(cls._table).order_by(index=r.desc(index)).limit(20).run(res.conn))

    @classmethod
    def find(cls, id):
        with pool.get_resource() as res:
            return r.table(cls._table).get(id).run(res.conn)

    @classmethod
    def filter(cls, predicate):
        with pool.get_resource() as res:
            return list(r.table(cls._table).filter(predicate).run(res.conn))

    @classmethod
    def filter_by_relation(cls, related_model, predicate, **kwargs):
        index = kwargs.get("index") or "id"
        without = kwargs.get("without") or {}
        with pool.get_resource() as res:
            return list(r.table(cls._table).eq_join(cls._pk, r.table(related_model._table),
                                                    index=index).without(without).zip().filter(predicate).run(res.conn))

    @classmethod
    def update(cls, id, fields):
        with pool.get_resource() as res:
            status = r.table(cls._table).get(id).update(fields).run(res.conn)
            if status['errors']:
                raise DatabaseProcessError("Could not complete the update action")
            return True

    @classmethod
    def delete(cls, id):
        with pool.get_resource() as res:
            status = r.table(cls._table).get(id).delete().run(res.conn)
            if status['errors']:
                raise DatabaseProcessError("Could not complete the delete action")
            return True

    @classmethod
    def feed(cls):
        with pool.get_resource() as res:
            return r.table(cls._table).changes().run(res.conn)
