from db.connection import get_connection


def add_tariff(
    club_id,
    service_id,
    source_id,
    product_type,
    days,
    start_time,
    end_time,
    price,
    price_type,
    duration_minutes,
    quantity,
    payment_unit,
    payment_mode,
    tariff_type,
    checked_at,
    note,
    conn=None
):
    own_connection = conn is None

    if own_connection:
        conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT tariff_id FROM tariff
            WHERE club_id=? AND service_id=? AND source_id=?
            AND product_type IS ? AND days IS ? AND start_time IS ?
            AND end_time IS ? AND price IS ? AND duration_minutes IS ?
            AND quantity IS ? AND checked_at=?
        ''', (
            club_id,
            service_id,
            source_id,
            product_type,
            days,
            start_time,
            end_time,
            price,
            duration_minutes,
            quantity,
            checked_at
        ))

        existing = cursor.fetchone()

        if existing:
            return False

        cursor.execute('''
            INSERT INTO tariff(
                club_id,
                service_id,
                source_id,
                product_type,
                days,
                start_time,
                end_time,
                price,
                price_type,
                duration_minutes,
                quantity,
                payment_unit,
                payment_mode,
                tariff_type,
                checked_at,
                note
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (
            club_id,
            service_id,
            source_id,
            product_type,
            days,
            start_time,
            end_time,
            price,
            price_type,
            duration_minutes,
            quantity,
            payment_unit,
            payment_mode,
            tariff_type,
            checked_at,
            note
        ))

        if own_connection:
            conn.commit()

        return True

    finally:
        if own_connection:
            conn.close()

    return True
def get_latest_court_tariffs():
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.name,
            t.product_type,
            t.days,
            t.start_time,
            t.end_time,
            t.price,
            t.duration_minutes,
            t.checked_at
        FROM tariff t
        JOIN club c
            ON t.club_id=c.club_id
        JOIN service s
            ON t.service_id=s.service_id
        WHERE s.service_name='Аренда корта'
        AND t.checked_at=(
            SELECT MAX(t2.checked_at)
            FROM tariff t2
            WHERE t2.club_id=t.club_id
            AND t2.service_id=t.service_id
        )
        ORDER BY c.name,t.product_type,t.days,t.start_time
    ''')

    rows=cursor.fetchall()
    conn.close()

    tariffs=[]

    for row in rows:
        tariffs.append({
            'club':row[0],
            'product_type':row[1],
            'days':row[2],
            'start_time':row[3],
            'end_time':row[4],
            'price':row[5],
            'duration_minutes':row[6],
            'checked_at':row[7]
        })

    return tariffs
def get_all_court_tariffs_history():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.club_id,
            c.name,
            s.service_name,
            t.product_type,
            t.days,
            t.start_time,
            t.end_time,
            t.price,
            t.duration_minutes,
            t.price_type,
            t.quantity,
            t.payment_unit,
            t.payment_mode,
            t.tariff_type,
            t.checked_at,
            src.url,
            t.note
        FROM tariff t
        JOIN club c
            ON t.club_id=c.club_id
        JOIN service s
            ON t.service_id=s.service_id
        LEFT JOIN source src
            ON t.source_id=src.source_id
        WHERE s.service_name='Аренда корта'
        ORDER BY c.name,t.checked_at
    ''')

    rows=cursor.fetchall()
    conn.close()

    result=[]

    for row in rows:

        result.append({
            'club_id':row[0],
            'club':row[1],
            'service':row[2],
            'product_type':row[3],
            'days':row[4],
            'start_time':row[5],
            'end_time':row[6],
            'price':row[7],
            'duration_minutes':row[8],
            'price_type':row[9],
            'quantity':row[10],
            'payment_unit':row[11],
            'payment_mode':row[12],
            'tariff_type':row[13],
            'checked_at':row[14],
            'source_url':row[15],
            'note':row[16]
        })

    return result