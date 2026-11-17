from statistics import mean,median

from repositories.tariff_repository import (
    get_latest_court_tariffs,
    get_all_court_tariffs_history
)

from repositories.club_service_repository import (
    get_latest_club_services,
    get_all_services_history
)
def normalize_price(price,duration_minutes):
    if price is None or duration_minutes is None:
        return None

    return price/duration_minutes*60


def get_price_analytics():
    tariffs=get_latest_court_tariffs()

    clubs={}

    for tariff in tariffs:
        club=tariff['club']

        price_60=normalize_price(
            tariff['price'],
            tariff['duration_minutes']
        )

        if price_60 is None:
            continue

        if club not in clubs:
            clubs[club]=[]

        clubs[club].append(price_60)

    club_stats={}

    for club,prices in clubs.items():
        club_stats[club]={
            'min_price':min(prices),
            'max_price':max(prices),
            'average_price':mean(prices),
            'median_price':median(prices),
            'tariff_count':len(prices)
        }

    # Средняя цена сначала считается для каждого клуба,
    # затем среднее берётся между клубами.
    # Так клуб с большим количеством тарифных строк
    # не получает больший вес.
    club_averages=[
        stats['average_price']
        for stats in club_stats.values()
    ]

    if not club_averages:
        return {
            'market':{},
            'clubs':{}
        }

    market_average=mean(club_averages)

    club_medians = [
        stats['median_price']
        for stats in club_stats.values()
    ]

    all_prices = [
        price
        for prices in clubs.values()
        for price in prices
    ]

    market_stats = {
        'average_price': market_average,
        'median_price': median(club_medians),
        'min_price': min(all_prices),
        'max_price': max(all_prices)
    }

    for club,stats in club_stats.items():

        if market_average!=0:
            price_index=(
                stats['average_price']
                /market_average
                *100
            )
        else:
            price_index=None

        stats['price_index']=price_index

    return {
        'market':market_stats,
        'clubs':club_stats
    }


def get_services_comparison():
    service_rows=get_latest_club_services()
    tariff_rows=get_latest_court_tariffs()

    clubs=set()
    services=set()

    for row in service_rows:
        clubs.add(row['club'])
        services.add(row['service'])

    # Наличие тарифа аренды автоматически
    # подтверждает наличие услуги "Аренда корта"
    for row in tariff_rows:
        clubs.add(row['club'])
        services.add('Аренда корта')

    clubs=sorted(clubs)
    services=sorted(services)

    comparison={}

    for service in services:
        comparison[service]={}

        for club in clubs:
            comparison[service][club]='Нет данных'

    # Сначала данные CLUB_SERVICE
    for row in service_rows:
        comparison[row['service']][row['club']]=row['status']

    # Если есть тариф аренды —
    # аренда корта точно существует
    for row in tariff_rows:
        comparison['Аренда корта'][row['club']]='Есть'

    return {
        'clubs':clubs,
        'services':comparison
    }

def get_competitor_changes():
    tariffs=get_all_court_tariffs_history()
    services=get_all_services_history()

    changes=[]

    clubs=set(row['club'] for row in tariffs)

    for club in clubs:
        club_tariffs=[
            row for row in tariffs
            if row['club']==club
        ]

        tariff_dates=sorted(set(
            row['checked_at'] for row in club_tariffs
        ))

        if len(tariff_dates)<2:
            continue

        previous_date=tariff_dates[-2]
        current_date=tariff_dates[-1]

        previous=[
            row for row in club_tariffs
            if row['checked_at']==previous_date
        ]

        current=[
            row for row in club_tariffs
            if row['checked_at']==current_date
        ]

        def tariff_key(row):
            return (
                row['service'] if 'service' in row else None,
                row['product_type'],
                row['days'],
                row['start_time'],
                row['end_time'],
                row['duration_minutes'],
                row['price_type'],
                row['quantity'],
                row['payment_unit'],
                row['payment_mode'],
                row['tariff_type']
            )

        previous_dict={
            tariff_key(row):row
            for row in previous
        }

        current_dict={
            tariff_key(row):row
            for row in current
        }

        for key,current_row in current_dict.items():
            if key not in previous_dict:
                continue

            previous_price=previous_dict[key]['price']
            current_price=current_row['price']

            if previous_price is None or current_price is None:
                continue

            if previous_price<=0 or previous_price==current_price:
                continue

            percent=(
                (current_price-previous_price)
                /previous_price*100
            )

            change_type='price_up' if percent>0 else 'price_down'

            changes.append({
                'club':club,
                'type':change_type,
'title':(
    f"{club} · {current_row['product_type']} · "
    f"{current_row['days']}, "
    f"{current_row['start_time']}–{current_row['end_time']} · "
    f"{previous_price:.0f} → {current_price:.0f} ₽ "
    f"({percent:+.1f}%)"
),
                'description':(
                    f"{current_row['product_type']}, "
                    f"{current_row['days']}, "
                    f"{current_row['start_time']}–"
                    f"{current_row['end_time']}: "
                    f"{previous_price:.0f} ₽ → "
                    f"{current_price:.0f} ₽ "
                    f"({percent:+.1f}%)"
                ),
                'date':current_date,
                'value':percent
            })

    changes=sorted(
        changes,
        key=lambda x:x['date'],
        reverse=True
    )

    return changes



def get_weekly_insights():
    changes=get_competitor_changes()

    insights=[]

    price_up=[
        change
        for change in changes
        if change['type']=='price_up'
    ]

    price_down=[
        change
        for change in changes
        if change['type']=='price_down'
    ]

    new_services=[
        change
        for change in changes
        if change['type']=='new_service'
    ]

    # Значимое повышение цены
    significant_growth=[
        change
        for change in price_up
        if change['value'] is not None
        and change['value']>=5
    ]

    if significant_growth:

        max_change=max(
            significant_growth,
            key=lambda x:x['value']
        )

        insights.append({
            'level':'warning',
            'title':'Цены конкурентов растут',
            'text':(
                f"Обнаружено повышение тарифа у "
                f"{max_change['club']} на "
                f"{max_change['value']:.1f}%. "
                f"Стоит проверить собственное ценовое "
                f"позиционирование, прежде чем менять тарифы."
            )
        })

    if price_down:

        insights.append({
            'level':'info',
            'title':'На рынке появились более низкие тарифы',
            'text':(
                'У одного или нескольких конкурентов '
                'обнаружено снижение цены. '
                'Имеет смысл проверить off-peak предложения '
                'и привлекательность собственных тарифов '
                'в непиковые часы.'
            )
        })

    if new_services:

        services=', '.join(
            sorted(
                set(
                    change['description']
                    for change in new_services
                )
            )
        )

        insights.append({
            'level':'success',
            'title':'Конкуренты расширяют предложение',
            'text':(
                f'На последней проверке появились новые '
                f'услуги: {services}. '
                f'Стоит оценить, являются ли они новым '
                f'рыночным стандартом или способом '
                f'дифференциации отдельных клубов.'
            )
        })

    if not changes:

        insights.append({
            'level':'info',
            'title':'Значимых изменений пока не обнаружено',
            'text':(
                'Для построения динамики нужны минимум '
                'две проверки одного клуба в разные даты. '
                'После следующего обновления здесь появятся '
                'автоматические выводы.'
            )
        })

    elif not insights:

        insights.append({
            'level':'info',
            'title':'Рынок остаётся относительно стабильным',
            'text':(
                'Обнаруженные изменения пока не требуют '
                'немедленной реакции. Рекомендуется '
                'продолжать мониторинг цен и продуктовых '
                'предложений конкурентов.'
            )
        })

    return insights