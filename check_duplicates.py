from db.connection import get_connection


def main():
    conn=get_connection()
    cursor=conn.cursor()

    # 1. Сколько всего тарифов Паделграда лежит в БД
    cursor.execute('''
        SELECT COUNT(*)
        FROM tariff t
        JOIN club c ON t.club_id=c.club_id
        WHERE c.name='Паделград'
    ''')

    total=cursor.fetchone()[0]

    print('Всего тарифов Паделграда в БД:',total)

    # 2. Ищем полностью одинаковые тарифы
    cursor.execute('''
        SELECT
            t.service_id,
            t.product_type,
            t.days,
            t.start_time,
            t.end_time,
            t.price,
            t.duration_minutes,
            t.quantity,
            t.checked_at,
            COUNT(*) as count_duplicates
        FROM tariff t
        JOIN club c ON t.club_id=c.club_id
        WHERE c.name='Паделград'
        GROUP BY
            t.service_id,
            t.product_type,
            t.days,
            t.start_time,
            t.end_time,
            t.price,
            t.duration_minutes,
            t.quantity,
            t.checked_at
        HAVING COUNT(*)>1
    ''')

    duplicates=cursor.fetchall()

    print('Количество групп дублей:',len(duplicates))

    if duplicates:
        print('\nНайдены дубли:')

        for row in duplicates:
            print(row)
    else:
        print('Дублей нет')

    conn.close()


if __name__=='__main__':
    main()