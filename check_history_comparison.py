from db.connection import get_connection


def make_key(row):
    return (
        row[2],   # product_type
        row[3],   # days
        row[4],   # start_time
        row[5],   # end_time
        row[7],   # duration_minutes
        row[8],   # price_type
        row[9],   # quantity
        row[10],  # payment_unit
        row[11],  # payment_mode
        row[12]   # tariff_type
    )


def main():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''
        SELECT
            c.name,
            t.checked_at,
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
            t.tariff_type
        FROM tariff t
        JOIN club c
            ON t.club_id=c.club_id
        JOIN service s
            ON t.service_id=s.service_id
        WHERE s.service_name='Аренда корта'
        AND c.name IN ('Паделград','Культ Падел')
        ORDER BY c.name,t.checked_at
    ''')

    rows=cursor.fetchall()

    conn.close()

    clubs={}

    for row in rows:

        club=row[0]

        if club not in clubs:
            clubs[club]=[]

        clubs[club].append(row)

    for club,club_rows in clubs.items():

        print('\n============================')
        print('КЛУБ:',club)
        print('============================')

        dates=sorted(
            set(row[1] for row in club_rows)
        )

        if len(dates)<2:
            print('Недостаточно исторических данных')
            continue

        previous_date=dates[-2]
        current_date=dates[-1]

        previous=[
            row for row in club_rows
            if row[1]==previous_date
        ]

        current=[
            row for row in club_rows
            if row[1]==current_date
        ]

        previous_dict={
            make_key(row):row
            for row in previous
        }

        current_dict={
            make_key(row):row
            for row in current
        }

        matched=set(previous_dict) & set(current_dict)

        new=set(current_dict)-set(previous_dict)

        missing=set(previous_dict)-set(current_dict)

        print('Предыдущая проверка:',previous_date)
        print('Текущая проверка:',current_date)

        print('\nКоличество тарифов:')
        print('Предыдущая:',len(previous))
        print('Текущая:',len(current))

        print('\nСопоставлено тарифов:',len(matched))
        print('Новые ключи:',len(new))
        print('Не найдены в новом снимке:',len(missing))

        print('\n--- ИЗМЕНЕНИЯ ЦЕН ---')

        changes=0

        for key in matched:

            old_price=previous_dict[key][6]
            new_price=current_dict[key][6]

            if old_price!=new_price:

                changes+=1

                print(
                    key[0],
                    key[1],
                    key[2],
                    key[3],
                    old_price,
                    '->',
                    new_price
                )

        if changes==0:
            print('Изменений цен не обнаружено')

        print('\n--- НОВЫЕ ПРЕДЛОЖЕНИЯ ---')

        for key in new:
            print(key)

        print('\n--- НЕ НАЙДЕНЫ В НОВОМ СНИМКЕ ---')

        for key in missing:
            print(key)


if __name__=='__main__':
    main()