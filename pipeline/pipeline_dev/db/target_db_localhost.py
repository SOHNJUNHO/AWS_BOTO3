
queries = {
    'create': {
        'actor': '''
            INSERT INTO actor_back VALUES (%s, %s, %s, %s, %s)
            ;
        ''',
        'film': '''
            INSERT INTO film_back VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ;
        '''
					}
    }
