import pandas as pd

def cursor_loader(db_connector, table_name, data):
    with db_connector as connected:
        create_query = connected.get_query('create', table_name)
        with connected.conn.cursor() as cur:
            cur.executemany(create_query, data)
            connected.conn.commit()



def pandas_loader(db_connector, table_name, data):
    data.to_sql(table_name +'_front', db_connector, if_exists='append', index=False)
    print(f'insert > {table_name}')
