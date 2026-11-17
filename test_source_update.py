from repositories.source_repository import update_source_check
from db.connection import get_connection


url='https://padelgrad.club/price'

update_source_check(
    url=url,
    status='success'
)

conn=get_connection()
cursor=conn.cursor()

cursor.execute('''
    SELECT
        source_name,
        last_checked_at,
        last_check_status,
        last_error
    FROM source
    WHERE url=?
''',(url,))

print(cursor.fetchone())

conn.close()