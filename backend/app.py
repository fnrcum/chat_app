from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit
from threading import Thread

global thread
thread = None
app = Flask(__name__)
app.config.from_object('config')
CORS(app)
with app.app_context():
    from models._models import TokenBlacklist, Pages, Permissions, User, jwt, dbSetup
    from resources import *
    dbSetup()


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix="/api/v1")


api.add_resource(TokenBlacklistResource, '/tokens')
api.add_resource(PermissionsResource, '/permissions')
api.add_resource(AuthLogin, '/auth/login')
api.add_resource(AuthRegister, '/auth/register')
api.add_resource(UsersResource, '/users')
api.add_resource(CreateChat, '/chats')
api.add_resource(ListChats, '/')

socketio = SocketIO(app)


def watch_chats():
    print('Watching db for new chats!')

    feed = Chat().feed()
    for chat in feed:
        chat['new_val']['created'] = str(chat['new_val']['created'])
        print(chat)
        socketio.emit('new_chat', chat)


if __name__ == '__main__':
    if thread is None:
        thread = Thread(target=watch_chats)
        thread.start()
    print('Running app')
    socketio.run(app, host='0.0.0.0', port=5001)
    # app.run(debug=True, port=5001)