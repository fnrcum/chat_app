import rethinkdb as r
from flask import current_app
from .rpool import RethinkPool

# RDB_HOST = 'gameservers.go.ro'  # '34.217.209.173'
# RDB_PORT = 28015
# RDB_DBNAME = 'fleet'
# RDB_TABLES = ['token_blacklist', 'permissions', 'users']
pool = RethinkPool(initial_conns=10, max_conns=100, host=current_app.config['RDB_HOST'],
                   port=current_app.config['RDB_PORT'], db=current_app.config['RDB_DBNAME'])


def _ensure_db(conn):
    # create database
    try:
        r.db_create(current_app.config['RDB_DBNAME']).run(conn)
        print("Database created successfully")
    except r.RqlRuntimeError:
        print("Database already exists")
        pass


# Function is for cross-checking database and table exists
def dbSetup():
    with pool.get_resource() as res:
        _ensure_db(res.conn)

        for table in current_app.config['RDB_TABLES']:
            try:
                r.table_create(table).run(res.conn)
                if table is "chat":
                    r.table_create(table).index_create("created").run(res.conn)
                print('Table: "{}" creation completed'.format(table))
            except Exception as e:
                error = '%s' % e
                print(error.split("in:")[0])
                pass
    print("DB setup done")
