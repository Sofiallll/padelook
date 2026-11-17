from db.connection import get_connection


def get_service_id_by_name(name):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT service_id
        FROM service
        WHERE service_name=?
    ''',(name,))

    result=cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return None