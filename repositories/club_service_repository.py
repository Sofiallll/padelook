from db.connection import get_connection


def add_club_service(
    club_id,
    service_id,
    source_id,
    checked_at,
    availability_status,
    conn=None
):
    own_connection = conn is None

    if own_connection:
        conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT club_service_id
            FROM club_service
            WHERE club_id=? AND service_id=? AND checked_at=?
        ''', (
            club_id,
            service_id,
            checked_at
        ))

        existing = cursor.fetchone()

        if existing:
            return False

        cursor.execute('''
            INSERT INTO club_service(
                club_id,
                service_id,
                source_id,
                checked_at,
                availability_status
            )
            VALUES(?,?,?,?,?)
        ''', (
            club_id,
            service_id,
            source_id,
            checked_at,
            availability_status
        ))

        if own_connection:
            conn.commit()

        return True

    finally:
        if own_connection:
            conn.close()

def get_latest_club_services():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.name,
            s.service_name,
            cs.availability_status,
            cs.checked_at
        FROM club_service cs
        JOIN club c
            ON cs.club_id=c.club_id
        JOIN service s
            ON cs.service_id=s.service_id
        WHERE cs.checked_at=(
            SELECT MAX(cs2.checked_at)
            FROM club_service cs2
            WHERE cs2.club_id=cs.club_id
            AND cs2.service_id=cs.service_id
        )
        ORDER BY c.name,s.service_name
    ''')

    rows=cursor.fetchall()
    conn.close()

    services=[]

    for row in rows:
        services.append({
            'club':row[0],
            'service':row[1],
            'status':row[2],
            'checked_at':row[3]
        })

    return services
def get_all_services_history():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.name,
            s.service_name,
            cs.availability_status,
            cs.checked_at
        FROM club_service cs
        JOIN club c
            ON cs.club_id=c.club_id
        JOIN service s
            ON cs.service_id=s.service_id
        ORDER BY c.name,cs.checked_at
    ''')

    rows=cursor.fetchall()
    conn.close()

    result=[]

    for row in rows:
        result.append({
            'club':row[0],
            'service':row[1],
            'status':row[2],
            'checked_at':row[3]
        })

    return result