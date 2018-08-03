import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = '2d*%^#ff{3015-916e-4b7}]8-8d7d-bfcf6(62!6|977c'

RDB_HOST = '34.217.209.173'  # 'localhost' # 'gameservers.go.ro'  #
RDB_PORT = 28015
RDB_DBNAME = 'chatapp'
RDB_TABLES = ['chats', 'permissions', 'users', 'pages']

BABEL_DEFAULT_LOCALE = 'en'

LANGUAGES = {
    'en': {'flag': 'gb', 'name': 'English'},
    'pt': {'flag': 'pt', 'name': 'Portuguese'},
    'es': {'flag': 'es', 'name': 'Spanish'},
    'de': {'flag': 'de', 'name': 'German'},
    'zh': {'flag': 'cn', 'name': 'Chinese'},
    'ru': {'flag': 'ru', 'name': 'Russian'}
}

#------------------------------
# GLOBALS FOR GENERAL APP's
#------------------------------
UPLOAD_FOLDER = basedir + '/app/static/uploads/'
IMG_UPLOAD_FOLDER = basedir + '/app/static/uploads/'
IMG_UPLOAD_URL = '/static/uploads/'
APP_THEME = ""                  # default
