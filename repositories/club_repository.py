from db.connection import get_connection


def get_club_id_by_name(name):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT club_id
        FROM club
        WHERE name=?
    ''',(name,))

    result=cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return None