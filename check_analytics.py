from analytics.competitors import (
    get_price_analytics,
    get_services_comparison
)


def main():

    # =========================
    # ЦЕНЫ
    # =========================

    analytics=get_price_analytics()

    print('--- РЫНОК ---')

    market=analytics['market']

    print(
        'Средняя цена:',
        round(market['average_price'],2)
    )

    print(
        'Медианная цена:',
        round(market['median_price'],2)
    )

    print(
        'Минимальная цена:',
        round(market['min_price'],2)
    )

    print(
        'Максимальная цена:',
        round(market['max_price'],2)
    )

    print()

    print('--- КЛУБЫ ---')

    for club,stats in analytics['clubs'].items():

        print()
        print(club)

        print(
            'Средняя:',
            round(stats['average_price'],2)
        )

        print(
            'Медиана:',
            round(stats['median_price'],2)
        )

        print(
            'Минимум:',
            round(stats['min_price'],2)
        )

        print(
            'Максимум:',
            round(stats['max_price'],2)
        )

        print(
            'Price Index:',
            round(stats['price_index'],2)
        )

        print(
            'Количество тарифов:',
            stats['tariff_count']
        )

    # =========================
    # УСЛУГИ
    # =========================

    print()
    print('--- УСЛУГИ ---')

    comparison=get_services_comparison()

    clubs=comparison['clubs']

    print(
        'Услуга |',
        ' | '.join(clubs)
    )

    for service,statuses in comparison['services'].items():

        values=[
            statuses[club]
            for club in clubs
        ]

        print(
            service,
            '|',
            ' | '.join(values)
        )


if __name__=='__main__':
    main()