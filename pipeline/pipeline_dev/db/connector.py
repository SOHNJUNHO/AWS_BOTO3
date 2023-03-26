#import psycopg2 as postgre
# import pymssql as mssql
# import pymysql as mysql

#class DBConnector:

#    def __init__(self, host, port, user, password, database):
#        self.conn_params = dict(
#            host = host,
#            port = port,
#            user = user,
#            password = password,
#            database = database
#        )
#        # self.conn =None

#    def _postgre_connect(self):
#        conn = postgre.connect(**self.conn_params)
#        return conn


import psycopg2 as postgre
# import pymssql as mssql
# import pymysql as mysql

from db import source_db_localhost
from db import target_db_localhost



class DBConnector:

    def __init__(self, location, host, port, user, password, database, engine):
        self.conn_params = dict(
            host = host,
            port = port,
            user = user,
            password = password,
            database = database
        )
        self.location = location
        self.engine = engine
        self.conn = None

        if self.location == 'localhost_source':
            if self.engine == 'postgre':
                self.queries = source_db_localhost.queries
                self.connect = self._postgre_connect
            else:
                raise RuntimeError(f"{self.engine} is not supported")
        elif self.location == 'localhost_target':
            if self.engine == 'postgre':
                self.queries = target_db_localhost.queries 
                self.connect = self._postgre_connect
            else:
                raise RuntimeError(f"{self.engine} is not supported")
        else:
            raise RuntimeError(f"{self.location} is not supported")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    # def _postgre_connect(self):
    #     conn = postgre.connect(**self.conn_params)
    #     return conn
    
    def _postgre_connect(self):
        self.conn = postgre.connect(**self.conn_params)

    def get_query(self, crud, query_name, preparam=None):
        _query = self.queries[crud][query_name]

        if preparam:
            return _query.format(**preparam)

        return _query