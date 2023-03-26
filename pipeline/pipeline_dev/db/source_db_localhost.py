
queries = {
    'read': {
        'actor': '''
            SELECT '{batch_month}' AS YYYYMM, * 
            FROM actor 
            WHERE TO_CHAR(CAST(last_update AS DATE), 'YYYYMM') = '{batch_month}'
            ;
        ''',
        'film': '''
            SELECT '{batch_month}' AS YYYYMM, * 
            FROM film 
            WHERE TO_CHAR(CAST(last_update AS DATE), 'YYYYMM') = '{batch_month}'
            ;
        '''}
}