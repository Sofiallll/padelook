from db.connection import get_connection


def main():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.name,
            s.service_name,
            cs.availability_status,
            src.url,
            cs.checked_at
        FROM club_service cs
        JOIN club c
            ON cs.club_id=c.club_id
        JOIN service s
            ON cs.service_id=s.service_id
        LEFT JOIN source src
            ON cs.source_id=src.source_id
        WHERE c.name IN ('Паделград','Культ Падел')
        ORDER BY c.name,s.service_name
    ''')

    rows=cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()


if __name__=='__main__':
    main()