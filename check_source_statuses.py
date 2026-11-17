from db.connection import get_connection


def main():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            source_name,
            url,
            last_checked_at,
            last_check_status,
            last_error
        FROM source
        WHERE last_checked_at IS NOT NULL
        ORDER BY source_id
    ''')

    rows=cursor.fetchall()

    print('--- СТАТУСЫ ИСТОЧНИКОВ ---')

    for row in rows:
        print(row)

    conn.close()


if __name__=='__main__':
    main()