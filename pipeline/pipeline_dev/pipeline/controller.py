from sqlalchemy import create_engine
from db.connector import DBConnector
from settings import DB_SETTINGS
from pipeline import extractor, load, transform


source_db = DBConnector(**DB_SETTINGS['source_db_localhost'])
target_db = DBConnector(**DB_SETTINGS['target_db_localhost'])

source_engine = \
    create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'\
        .format(\
            user = "postgres"
            , password = "208300"
            , host = "127.0.0.1"
            , port = "5432"
            , database = "dvdrental")
            )
target_engine = \
    create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'\
        .format(\
            user = "postgres"
            , password = "208300"
            , host = "127.0.0.1"
            , port = "5432"
            , database = "sample")
            )



def etl(batch_month, read_option = 'pandas'):
        if read_option == 'cursor':
            _temp = extractor.cursor_extractor(db_connector = source_db, table_name = 'film', batch_month = batch_month)
        elif read_option == 'pandas':
            _temp = extractor.pandas_extractor(db_connector = source_db, table_name = 'film', batch_month = batch_month)
        print(_temp[:1])


        if read_option == 'pandas' :
           _temp1 = transform.pandas_transformer(data=_temp)


        if read_option == 'cursor':
            load.cursor_loader(db_connector = target_db, table_name = 'film', data = _temp1)
        elif read_option == 'pandas':
            load.pandas_loader(db_connector = target_engine, table_name = 'film', data = _temp1)




#def extractor(db_connector, table_name, batch_month):
#    with db_connector as connected:
#        read_query = connected.get_query('read', table_name, {'batch_month': batch_month})
#        with connected.conn.cursor() as cur:
#            cur.execute(read_query)
#            result_all = cur.fetchall()
#            return result_all 



#def etl(batch_month):
 #   with source_db as source_connected:
  #      for table in TABLE_LIST:
   #         read_query = source_connected.get_query('read', table, {'batch_month': batch_month})
    #        print(read_query)
            
     #       with source_connected.conn.cursor() as source_cur:
      #          source_cur.execute(read_query)
       #         result_all = source_cur.fetchall()
        #        print(result_all[:1])


#def etl(bathch_month):
 #   for table in TABLE_LIST:
  #      _temp = extractor(db_connector=source_db, table_name=table, batch_month=bathch_month)
        
    #    print(_temp[:1])
            
 

   
#def extractor(db_connector, table_name, batch_month):                
     #with db_connector as connected:
        # read_query = connected.get_query('read', table_name, {'batch_month': batch_month})
         #with connected.conn as conn:
           # pdf = pd.read_sql(read_query, conn)
            #return pdf

            
            







