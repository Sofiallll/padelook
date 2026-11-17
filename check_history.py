from db.connection import get_connection


def main():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.name,
            t.checked_at,
            COUNT(*) as tariff_count
        FROM tariff t
        JOIN club c
            ON t.club_id=c.club_id
        WHERE c.name IN ('Паделград','Культ Падел')
        GROUP BY c.name,t.checked_at
        ORDER BY c.name,t.checked_at
    ''')

    print('--- ИСТОРИЯ ТАРИФОВ ---')

    for row in cursor.fetchall():
        print(row)

    conn.close()


if __name__=='__main__':
    main()