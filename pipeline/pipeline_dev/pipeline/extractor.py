import pandas as pd

def cursor_extractor(db_connector, table_name, batch_month):
    with db_connector as connected:
        read_query = connected.get_query('read', table_name, {'batch_month': batch_month})
        with connected.conn.cursor() as cur:
            cur.execute(read_query)
            result_all = cur.fetchall()
            return result_all

def pandas_extractor(db_connector, table_name, batch_month):
    with db_connector as connected:
        read_query = connected.get_query('read', table_name, {'batch_month': batch_month})
        with connected.conn as conn:
            pdf = pd.read_sql(read_query, conn)
            return pdf




# def pandas_transformer(db_connector, table, batch_month):
#   with db_connector as connected:
# 