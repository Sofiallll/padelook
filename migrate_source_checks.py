from db.connection import get_connection


def migrate_source():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('PRAGMA table_info(source)')

    columns=[
        row[1]
        for row in cursor.fetchall()
    ]

    new_columns=[
        ('last_checked_at','TEXT'),
        ('last_check_status','TEXT'),
        ('last_error','TEXT')
    ]

    for column_name,column_type in new_columns:

        if column_name not in columns:

            cursor.execute(
                f'ALTER TABLE source ADD COLUMN '
                f'{column_name} {column_type}'
            )

            print('Добавлен столбец:',column_name)

        else:
            print('Столбец уже существует:',column_name)

    conn.commit()

    print('\n--- НОВАЯ СТРУКТУРА SOURCE ---')

    cursor.execute('PRAGMA table_info(source)')

    for column in cursor.fetchall():
        print(column[1],column[2])

    conn.close()


if __name__=='__main__':
    migrate_source()