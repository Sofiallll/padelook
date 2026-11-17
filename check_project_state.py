import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR=Path(__file__).resolve().parent
DB_PATH=BASE_DIR/'data'/'padel.db'


def create_backup():

    if not DB_PATH.exists():
        raise FileNotFoundError('База данных не найдена')

    backup_path=BASE_DIR/'data'/'padel_backup_before_padelook.db'

    if backup_path.exists():
        time=datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path=BASE_DIR/'data'/f'padel_backup_{time}.db'

    source=sqlite3.connect(DB_PATH)
    backup=sqlite3.connect(backup_path)

    source.backup(backup)

    source.close()
    backup.close()

    print('Резервная копия создана:')
    print(backup_path.name)


def check_database():

    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    tables=[
        'club',
        'source',
        'service',
        'club_service',
        'tariff'
    ]

    print('\n--- КОЛИЧЕСТВО ЗАПИСЕЙ ---')

    for table in tables:

        cursor.execute(
            f'SELECT COUNT(*) FROM {table}'
        )

        count=cursor.fetchone()[0]

        print(table,':',count)

    # Структура SOURCE
    print('\n--- СТРУКТУРА SOURCE ---')

    cursor.execute('PRAGMA table_info(source)')

    for column in cursor.fetchall():
        print(column[1],column[2])

    # Источники
    print('\n--- ИСТОЧНИКИ ---')

    cursor.execute('''
        SELECT source_id,source_name,url
        FROM source
        ORDER BY source_id
    ''')

    for row in cursor.fetchall():
        print(row)

    # Клубы
    print('\n--- КЛУБЫ ---')

    cursor.execute('''
        SELECT club_id,name
        FROM club
        ORDER BY club_id
    ''')

    for row in cursor.fetchall():
        print(row)

    # Даты тарифов
    print('\n--- ДАТЫ ПРОВЕРКИ ТАРИФОВ ---')

    cursor.execute('''
        SELECT DISTINCT checked_at
        FROM tariff
        ORDER BY checked_at
    ''')

    for row in cursor.fetchall():
        print(row[0])

    # Даты услуг
    print('\n--- ДАТЫ ПРОВЕРКИ УСЛУГ ---')

    cursor.execute('''
        SELECT DISTINCT checked_at
        FROM club_service
        ORDER BY checked_at
    ''')

    for row in cursor.fetchall():
        print(row[0])

    conn.close()


def main():

    create_backup()
    check_database()


if __name__=='__main__':
    main()