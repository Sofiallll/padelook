
from collections import defaultdict
from statistics import mean

import pandas as pd
import streamlit as st

from analytics.competitors import (
    get_price_analytics,
    get_competitor_changes
)
from repositories.tariff_repository import get_all_court_tariffs_history


st.markdown('''
<style>
    
.market-hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(125deg, #E5EAD9 0%, #F0F0E5 58%, #F4E5E6 100%);
    border: 1px solid rgba(131, 143, 88, 0.15);
    border-radius: 28px;
    padding: 40px 42px;
    margin-bottom: 36px;
    box-shadow:
        0 12px 30px rgba(55, 65, 45, 0.055),
        0 28px 55px rgba(55, 65, 45, 0.035),
        inset 0 1px 0 rgba(255, 255, 255, 0.7);
    transition: box-shadow 0.3s ease;
}

.market-hero::after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    right: -65px;
    top: -95px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(249, 209, 217, 0.65), transparent 70%);
    pointer-events: none;
}

.market-hero:hover {
    box-shadow:
        0 16px 36px rgba(55, 65, 45, 0.075),
        0 30px 60px rgba(55, 65, 45, 0.045);
}


    .market-hero-label {
        color: #69764F;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .market-hero h1 {
        color: #30372F;
        font-size: 42px;
        font-weight: 750;
        letter-spacing: -0.04em;
        margin: 0 0 12px 0;
        padding: 0;
    }

    .market-hero p {
        color: #58614E;
        font-size: 16px;
        margin: 0;
    }

    .market-section {
        margin-top: 28px;
        margin-bottom: 18px;
    }

    .market-section-label {
        color: #838F58;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .market-section h2 {
        font-size: 28px;
        color: #30372F;
        letter-spacing: -0.03em;
        margin: 0;
    }

    .market-section p {
        color: #7A7D72;
        font-size: 14px;
        margin-top: 8px;
    }

    
/* Объёмные карточки с ценами */

[data-testid="stMetric"] {
    min-height: 145px;
    border-radius: 22px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.55);
    box-shadow:
        0 8px 18px rgba(55, 65, 45, 0.045),
        0 20px 38px rgba(55, 65, 45, 0.035),
        inset 0 1px 0 rgba(255, 255, 255, 0.65);
    transition:
        transform 0.3s ease,
        box-shadow 0.3s ease,
        border-color 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-6px);
    border-color: rgba(131, 143, 88, 0.25);
    box-shadow:
        0 14px 28px rgba(55, 65, 45, 0.09),
        0 26px 45px rgba(55, 65, 45, 0.06);
}

/* Цвета карточек */

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {
    background: linear-gradient(145deg, #F0F3E8, #DFE7D1);
}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
    background: linear-gradient(145deg, #FBECEF, #F3DCE2);
}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {
    background: linear-gradient(145deg, #F8F5EC, #EBE6D8);
}

[data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
> [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] {
    background: linear-gradient(145deg, #F0F3E8, #DFE7D1);
}

/* Текст карточек */

[data-testid="stMetricLabel"] {
    font-size: 14px;
    font-weight: 600;
    color: #596151;
}

[data-testid="stMetricValue"] {
    font-size: 36px;
    font-weight: 800;
    color: #30372F;
    letter-spacing: -0.04em;
}

/* Отключение анимации при соответствующей настройке системы */

@media (prefers-reduced-motion: reduce) {
    [data-testid="stMetric"] {
        transition: none;
    }

    [data-testid="stMetric"]:hover {
        transform: none;
    }
}



    [data-testid="stExpander"] {
        background: #FFFEFC;
        border-radius: 16px;
        border: 1px solid #E6E2D9;
    }
    

/* Лента изменений */

[data-testid="stExpander"] {
    background: linear-gradient(135deg, #FFFEFC 0%, #F8F7F1 100%);
    border: 1px solid #E8E6DC;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(55, 65, 45, 0.045);
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

[data-testid="stExpander"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(55, 65, 45, 0.09);
}

[data-testid="stExpander"] summary {
    padding: 6px 12px;
}

[data-testid="stExpander"] summary p {
    font-size: 15px;
    font-weight: 700;
    color: #394334;
    letter-spacing: -0.2px;
}

[data-testid="stExpander"] details[open] {
    background: #FFFEFC;
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stExpander"] {
        transition: none;
    }

    [data-testid="stExpander"]:hover {
        transform: none;
    }
}


/* Лента изменений */

[data-testid="stExpander"] {
    background: #FFFEFC;
    border: 1px solid #E8E5DD;
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 3px 12px rgba(48, 53, 43, 0.035);
    margin-bottom: 12px;
    transition: all 0.25s ease;
}

[data-testid="stExpander"]:hover {
    border-color: #C9D0B8;
    box-shadow: 0 6px 20px rgba(48, 53, 43, 0.06);
    transform: translateY(-1px);
}

[data-testid="stExpander"] summary {
    padding: 9px 12px;
}

[data-testid="stExpander"] summary p {
    font-size: 15px !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
    letter-spacing: 0 !important;
    color: #48533E;
}

[data-testid="stExpander"][open] {
    border-color: #C9D0B8;
}

[data-testid="stExpander"][open] summary {
    background: #F3F5ED;
}

[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 8px 16px 16px;
}

/* Повышение цены */

[data-testid="stExpander"]:has(.price-up) {
    border-left: 3px solid #A6B58A;
}

/* Снижение цены */

[data-testid="stExpander"]:has(.price-down) {
    border-left: 3px solid #E4B7C1;
}

[data-testid="stExpander"]:has(.price-down)[open] summary {
    background: #FAEFF1;
}


</style>
''',unsafe_allow_html=True)


st.markdown('''
<div class="market-hero">
    <div class="market-hero-label">PADELOOK / АНАЛИТИКА РЫНКА</div>
    <h1>Обзор рынка</h1>
    <p>Цены и изменения на рынке падел-клубов Санкт-Петербурга.</p>
</div>
''',unsafe_allow_html=True)


price_data=get_price_analytics()
market=price_data['market']
clubs=price_data['clubs']

if not market:
    st.warning('В базе пока недостаточно данных для аналитики.')
    st.stop()


st.markdown('''
<div class="market-section">
    <div class="market-section-label">01 / РЫНОК</div>
    <h2>Цены на аренду кортов</h2>
</div>
''',unsafe_allow_html=True)

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric('Средняя цена',f"{market['average_price']:.0f} ₽")
    st.caption(
        'Средняя по опубликованным тарифам аренды '
        'с равным весом каждого клуба'
    )

with col2:
    st.metric('Медианная цена',f"{market['median_price']:.0f} ₽")
    st.caption('Медиана клубных медиан')

with col3:
    st.metric('Минимальный тариф',f"{market['min_price']:.0f} ₽")
    st.caption('Минимальная опубликованная цена за 60 минут')

with col4:
    st.metric('Максимальный тариф',f"{market['max_price']:.0f} ₽")
    st.caption('Максимальная опубликованная цена за 60 минут')


st.divider()

st.markdown('''
<div class="market-section">
    <div class="market-section-label">02 / МОНИТОРИНГ</div>
    <h2>Лента изменений конкурентов</h2>
    <p>Что изменилось между двумя последними проверками.</p>
</div>
''',unsafe_allow_html=True)

st.cache_data.clear()
changes=get_competitor_changes()

if not changes:
    st.info(
        'Пока недостаточно истории для сравнения. '
        'После следующего обновления данных здесь появятся изменения.'
    )

else:
    club_options=sorted(set(change['club'] for change in changes))
    type_options=sorted(set(change['type'] for change in changes))
    date_options=sorted(set(change['date'] for change in changes))

    col1,col2,col3=st.columns(3)

    with col1:
        selected_clubs=st.multiselect(
            'Клубы',
            club_options,
            default=club_options
        )

    with col2:
        selected_types=st.multiselect(
            'Типы изменений',
            type_options,
            default=type_options,
            format_func=lambda x:{
                'price_up':'Повышение цены',
                'price_down':'Снижение цены',
                'new_service':'Новая услуга',
                'new_tariff':'Новый тариф'
            }.get(x,x)
        )

    with col3:
        selected_dates=st.multiselect(
            'Даты',
            date_options,
            default=date_options
        )

    filtered_changes=[
        change for change in changes
        if change['club'] in selected_clubs
        and change['type'] in selected_types
        and change['date'] in selected_dates
    ]

    st.caption(f'Найдено событий: {len(filtered_changes)}')

    if not filtered_changes:
        st.markdown('''
        <div style="background-color:#F1F2E6;padding:16px 18px;border-radius:12px;color:#46513B;">
            По выбранным фильтрам изменений не найдено.
        </div>
        ''', unsafe_allow_html=True)

    for change in filtered_changes:
        if change['type'] == 'price_up':
            icon = '↑'
            color_class = 'price-up'
        elif change['type'] == 'price_down':
            icon = '↓'
            color_class = 'price-down'
        else:
            icon = '+'
            color_class = 'price-other'

        with st.expander(f"{icon} {change['title']}"):
            st.markdown(
                f'<span class="{color_class}"></span>',
                unsafe_allow_html=True
            )
            st.write(change['description'])
            st.caption(f"Клуб: {change['club']}")
            st.caption(f"Дата проверки: {change['date']}")

st.divider()

st.markdown('''
<div class="market-section">
    <div class="market-section-label">03 / ДИНАМИКА</div>
    <h2>Динамика средних цен на рынке</h2>
    <p>Средняя стоимость аренды за 60 минут по клубам с доступной историей наблюдений.</p>
</div>
''',unsafe_allow_html=True)

history=get_all_court_tariffs_history()
prices_by_date=defaultdict(lambda: defaultdict(list))

for row in history:
    price=row['price']
    duration=row['duration_minutes']

    if price is None or duration is None or duration<=0:
        continue

    prices_by_date[row['checked_at']][row['club']].append(
        price/duration*60
    )

chart_rows=[]

for date,club_prices in sorted(prices_by_date.items()):
    averages=[
        mean(prices)
        for prices in club_prices.values()
        if prices
    ]

    if averages:
        chart_rows.append({
            'Дата':date,
            'Средняя цена, ₽':round(mean(averages))
        })

if len(chart_rows)>=2:
    chart_df=pd.DataFrame(chart_rows).set_index('Дата')
    st.line_chart(chart_df,color='#838F58')

    st.caption(
        'Среднее рассчитывается сначала внутри каждого клуба, '
        'затем между клубами с наблюдениями на соответствующую дату. '
        'Состав клубов между датами может различаться.'
    )
else:
    st.info(
        'Для построения динамики необходимы наблюдения '
        'минимум за две даты.'
    )
