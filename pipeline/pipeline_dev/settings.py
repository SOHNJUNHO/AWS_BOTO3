


DB_SETTINGS = {
    'localhost_postgre_query' : {
        # 'location' : 'localhost',
        # 'engine' : 'postgre',
        'host' : "127.0.0.1",
        'port' : "5432",
        'user' : "postgres",
        'password' : "208300",
        'database' : "dvdrental"
    },
    'source_db_localhost' : {
        'location' : 'localhost_source',
        'host' : "127.0.0.1",
        'port' : "5432",
        'user' : "postgres",
        'password' : "208300",
        'database' : "dvdrental",
        'engine' : 'postgre'
    },
    'target_db_localhost' : {
        'location' : 'localhost_target',
        'host' : "127.0.0.1",
        'port' : "5432",
        'user' : "postgres",
        'password' : "208300",
        'database' : "sample",
        'engine' : 'postgre'
    }
}