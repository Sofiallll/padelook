from datetime import datetime

from db.connection import get_connection


def get_source_id_by_url(url):
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT source_id
        FROM source
        WHERE url=?
    ''',(url,))

    result=cursor.fetchone()
    conn.close()

    if result:
        return result[0]

    return None


def update_source_check(url,status,error=None):

    if status not in ('success','failed','parse_error'):
        raise ValueError('Некорректный статус проверки')

    checked_at=datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        UPDATE source
        SET
            last_checked_at=?,
            last_check_status=?,
            last_error=?
        WHERE url=?
    ''',(
        checked_at,
        status,
        error,
        url
    ))

    updated=cursor.rowcount

    conn.commit()
    conn.close()

    if updated==0:
        raise ValueError(
            f'Источник {url} не найден в БД'
        )

    return True