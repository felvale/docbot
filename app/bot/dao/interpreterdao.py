'''
Module responsible for fetching DB data for de interpreter workers
'''
from app.db.dbutils import DBUtils, MaxConnectionException

GET_INTENTION_QUERY = 'SELECT int.intention_name, int.intention_module, '   \
                    + 'ts_rank(rel.intention_tsvector, to_tsquery(%s), 1) AS RANK '    \
                    + 'FROM intentions int '   \
                    + 'JOIN intentions_rel rel on rel.intention_id = int.intention_id ' \
                    + 'WHERE rel.intention_tsvector @@ to_tsquery(%s) ' \
                    + 'ORDER BY RANK DESC'

def get_intention(intext, useand):
    '''
    Function to attempt to determine witch intention best suits the input
    '''
    swap_to = None
    if useand:
        swap_to = ' & '
    else:
        swap_to = ' | '

    adjusted_text = str.replace(intext, ' ', swap_to)
    conn = None
    cur = None
    try:
        conn = DBUtils.get_instance().get_connection()
        cur = conn.cursor()
        cur.execute(GET_INTENTION_QUERY, (adjusted_text, adjusted_text,))
        result = cur.fetchall()
        #return True for intention found, intention name and intention module
        #of the highest ranked intention
        if result:
            return True, result[0][0], result[0][1]

        return False, None, None

    except MaxConnectionException:
        print('Exceeded max DB connection Pool')
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            DBUtils.get_instance().close_connection(conn)

    return False, None, None
