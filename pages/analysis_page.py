import pandas as pd
import altair as alt
import streamlit as st
st.markdown('''
<style>
    [data-testid="stAlert"],
    [data-testid="stAlert"] > div,
    [data-testid="stAlert"] [data-testid="stAlertContent"] {
        background: #E8EDDF !important;
        background-color: #E8EDDF !important;
        color: #384331 !important;
    }

    [data-testid="stAlert"] {
        border: none !important;
        border-left: 3px solid #838F58 !important;
        border-radius: 12px !important;
        padding: 18px 22px !important;
        margin: 16px 0 24px !important;
        box-shadow: none !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] svg {
        color: #384331 !important;
    }
</style>
''',unsafe_allow_html=True)


def green_notice(message):
    st.markdown(
        f'<div style="background:#E8EDDF;color:#384331;'
        f'border-left:3px solid #838F58;border-radius:12px;'
        f'padding:18px 22px;margin:16px 0 24px;">'
        f'{message}</div>',
        unsafe_allow_html=True
    )



def style_service_status(value):
    if value=='Есть':
        return 'background-color: #E4EBD9; color: #48533E'

    if value=='Нет':
        return 'background-color: #F5E3E7; color: #79565E'

    if value=='Нет данных':
        return 'background-color: #F0EBDF; color: #777368'

    return ''



from analytics.competitors import (
    get_price_analytics,
    get_services_comparison
)

st.markdown('''
<style>
    .analysis-hero {
        background: linear-gradient(115deg,#E5EAD9 0%,#F1EDE4 57%,#F5E2E6 100%);
        border: 1px solid #E1E2D6;
        border-radius: 28px;
        padding: 42px 44px;
        margin-bottom: 46px;
        box-shadow: 0 14px 32px rgba(66,72,55,0.045);
    }

    .analysis-hero-label, .analysis-section-label {
        color: #788558;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .analysis-hero h1 {
        color: #30372F;
        font-size: 40px !important;
        font-weight: 700 !important;
        letter-spacing: -0.035em;
        line-height: 1.2;
        margin: 14px 0 12px;
        padding: 0;
    }

    .analysis-hero p {
        color: #626B5B;
        font-size: 16px;
        line-height: 1.6;
        margin: 0;
    }

    .analysis-section {
        margin-top: 42px;
        margin-bottom: 24px;
    }

    .analysis-section h2 {
        color: #30372F;
        font-size: 27px !important;
        font-weight: 650 !important;
        letter-spacing: -0.025em;
        line-height: 1.3;
        margin: 10px 0 0;
    }

    [data-testid="stMetric"] {
        min-height: 135px;
        border-radius: 20px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.7);
        box-shadow: 0 8px 24px rgba(55,63,48,0.045);
        transition: transform 0.2s ease,box-shadow 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(55,63,48,0.075);
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
    > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {
        background: #E8EDDE;
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
    > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
        background: #F5E4E8;
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
    > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {
        background: #F0ECE2;
    }

    [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"])
    > [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] {
        background: #E8EDDE;
    }

    [data-testid="stMetricLabel"] {
        color: #5E6659;
        font-size: 14px;
        font-weight: 500;
    }

    [data-testid="stMetricValue"] {
        color: #30372F;
        font-size: 31px;
        font-weight: 650;
        letter-spacing: -0.035em;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E6E4DB;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 5px 18px rgba(55,63,48,0.035);
    }

    [data-testid="stExpander"] {
        border: 1px solid #E6E4DB;
        border-radius: 16px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    [data-testid="stCaptionContainer"] {
        color: #85867E;
        line-height: 1.6;
    }

    [data-testid="stSelectbox"] {
        margin-bottom: 10px;
    }

    hr {
        border-color: #E8E4DC !important;
        margin: 34px 0 12px !important;
    }

    @media (max-width: 800px) {
        .analysis-hero { padding: 28px 24px; }
        .analysis-hero h1 { font-size: 32px !important; }
        .analysis-section { margin-top: 30px; }
    }

    @media (prefers-reduced-motion: reduce) {
        [data-testid="stMetric"] { transition: none; }
        [data-testid="stMetric"]:hover { transform: none; }
    }
</style>
''',unsafe_allow_html=True)

st.markdown('''
<div class="analysis-hero">
    <div class="analysis-hero-label">PADELOOK / КОНКУРЕНТНЫЙ АНАЛИЗ</div>
    <h1>Анализ конкурентов</h1>
    <p>Ценовое позиционирование и предложения клубов.</p>
</div>
''',unsafe_allow_html=True)


price_data=get_price_analytics()
market=price_data['market']
clubs=price_data['clubs']


if not market:
    st.warning('В базе пока недостаточно данных для аналитики.')
    st.stop()

st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">01 / АНАЛИЗ</div>
    <h2>Price Index</h2>
</div>
''',unsafe_allow_html=True)

st.write(
    'Показывает ценовое позиционирование клуба относительно '
    'среднего уровня рассматриваемого рынка. '
    '**Средний уровень рынка = 100.**'
)


price_index_data=[]

for club,stats in clubs.items():

    price_index_data.append({
        'Клуб':club,
        'Price Index':round(
            stats['price_index'],
            1
        ),
        'Средняя цена, ₽':round(
            stats['average_price']
        ),
        'Медиана, ₽':round(
            stats['median_price']
        ),
        'Минимум, ₽':round(
            stats['min_price']
        ),
        'Максимум, ₽':round(
            stats['max_price']
        )
    })


price_index_df=pd.DataFrame(
    price_index_data
)

price_index_df=price_index_df.sort_values(
    'Price Index'
)


chart=alt.Chart(price_index_df).mark_bar(
    color='#838F58',
    cornerRadiusEnd=7,
    size=28
).encode(
    x=alt.X(
        'Price Index:Q',
        title='Price Index',
        scale=alt.Scale(domain=[0, 135]),
        axis=alt.Axis(
            values=[0, 20, 40, 60, 80, 100, 120],
            grid=False,
            labelFontSize=12,
            titleFontSize=13
        )
    ),
    y=alt.Y(
        'Клуб:N',
        sort='-x',
        title=None,
        axis=alt.Axis(labelFontSize=13)
    ),
    tooltip=[
        alt.Tooltip('Клуб:N'),
        alt.Tooltip('Price Index:Q',format='.1f')
    ]
)

labels=alt.Chart(price_index_df).mark_text(
    align='left',
    baseline='middle',
    dx=12,
    fontSize=13,
    fontWeight='normal',
    color='#48533E'
).encode(
    x='Price Index:Q',
    y=alt.Y('Клуб:N',sort='-x'),
    text=alt.Text('Price Index:Q',format='.1f')
)

market_line=alt.Chart(
    pd.DataFrame({'level':[100]})
).mark_rule(
    color='#D6A6B2',
    strokeWidth=2,
    strokeDash=[5,5]
).encode(
    x='level:Q'
)

st.altair_chart(
    (chart+labels+market_line).properties(height=300),
    use_container_width=True
)

st.caption('Розовая пунктирная линия — средний уровень рынка (100).')


st.dataframe(
    price_index_df,
    hide_index=True,
    use_container_width=True
)


st.caption(
    'Средняя цена клуба — средняя цена по опубликованным '
    'тарифам аренды, а не фактическая средняя стоимость '
    'всех бронирований.'
)


st.divider()

st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">02 / АНАЛИЗ</div>
    <h2>Карточка клуба</h2>
</div>
''',unsafe_allow_html=True)


selected_club=st.selectbox(
    'Выберите клуб',
    list(clubs.keys())
)

club_stats=clubs[selected_club]

st.markdown('''
<style>
    .club-summary {
        margin-top: 12px;
        margin-bottom: 24px;
    }

    .club-summary [data-testid="stMetric"] {
        min-height: 132px;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.7);
        box-shadow: none;
    }

    .club-summary [data-testid="stMetricLabel"] {
        font-size: 14px;
        font-weight: 500;
    }

    .club-summary [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 650;
    }

    .club-position {
        background: #F0F1E8;
        border-left: 3px solid #838F58;
        border-radius: 12px;
        padding: 18px 22px;
        margin: 20px 0 28px 0;
        color: #48533E;
        font-size: 15px;
        line-height: 1.7;
    }
</style>
''',unsafe_allow_html=True)

col1,col2,col3,col4=st.columns(4,gap='medium')

with col1:
    with st.container():
        st.metric(
            'Средняя цена',
            f"{club_stats['average_price']:.0f} ₽"
        )

with col2:
    with st.container():
        st.metric(
            'Медианная цена',
            f"{club_stats['median_price']:.0f} ₽"
        )

with col3:
    with st.container():
        st.metric(
            'Price Index',
            f"{club_stats['price_index']:.1f}"
        )

with col4:
    with st.container():
        st.metric(
            'Количество тарифов',
            club_stats['tariff_count']
        )

if club_stats['price_index']>100:
    difference=club_stats['price_index']-100

    position_text=(
        f'Средняя цена по опубликованным тарифам клуба '
        f'примерно на {difference:.1f}% выше среднего '
        f'уровня рассматриваемого рынка.'
    )

elif club_stats['price_index']<100:
    difference=100-club_stats['price_index']

    position_text=(
        f'Средняя цена по опубликованным тарифам клуба '
        f'примерно на {difference:.1f}% ниже среднего '
        f'уровня рассматриваемого рынка.'
    )

else:
    position_text=(
        'Средняя цена клуба соответствует '
        'среднему уровню рассматриваемого рынка.'
    )

st.markdown(
    f'<div class="club-position">{position_text}</div>',
    unsafe_allow_html=True
)

st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">03 / АНАЛИЗ</div>
    <h2>Сравнение услуг</h2>
</div>
''',unsafe_allow_html=True)


comparison=get_services_comparison()

club_names=comparison['clubs']
services=comparison['services']


services_table=[]


for service,statuses in services.items():

    row={
        'Услуга':service
    }

    for club in club_names:
        row[club]=statuses[club]

    services_table.append(row)


services_df=pd.DataFrame(
    services_table
)


styled_services=services_df.style.map(
    style_service_status,
    subset=club_names
)

st.dataframe(
    styled_services,
    hide_index=True,
    use_container_width=True
)


st.caption(
    '«Нет данных» означает, что наличие или отсутствие услуги '
    'пока не подтверждено открытыми источниками.'
)

# =========================
# ДИНАМИКА ЦЕН КЛУБА
# =========================

from collections import defaultdict
from statistics import mean
from repositories.tariff_repository import get_all_court_tariffs_history

st.divider()
st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">04 / АНАЛИЗ</div>
    <h2>Динамика цен клуба</h2>
</div>
''',unsafe_allow_html=True)

history=get_all_court_tariffs_history()

history_clubs=sorted(set(
    row['club'] for row in history
))

history_club=st.selectbox(
    'Выберите клуб для анализа динамики',
    history_clubs,
    key='history_club'
)

prices_by_date=defaultdict(list)

for row in history:
    if row['club']!=history_club:
        continue

    price=row['price']
    duration=row['duration_minutes']

    if price is None or duration is None or duration<=0:
        continue

    prices_by_date[row['checked_at']].append(
        price/duration*60
    )

chart_rows=[]

for date,prices in sorted(prices_by_date.items()):
    chart_rows.append({
        'Дата':date,
        'Средняя цена, ₽':round(mean(prices))
    })

if len(chart_rows)>=2:
    chart_df=pd.DataFrame(chart_rows).set_index('Дата')
    plot_df = chart_df.reset_index()
    date_col = plot_df.columns[0]
    price_col = plot_df.columns[1]

    plot_df[date_col] = pd.to_datetime(plot_df[date_col])

    line=alt.Chart(plot_df).mark_line(
        color='#838F58',
        strokeWidth=3
    ).encode(
        x=alt.X(
            f'{date_col}:T',
            title=None,
            axis=alt.Axis(
                format='%d.%m.%Y',
                labelAngle=0,
                values=plot_df[date_col].tolist()
            )
        ),
        y=alt.Y(
            f'{price_col}:Q',
            title='Средняя цена, ₽',
            scale=alt.Scale(zero=False)
        ),
        tooltip=[
            alt.Tooltip(f'{date_col}:T',title='Дата',format='%d.%m.%Y'),
            alt.Tooltip(f'{price_col}:Q',title='Средняя цена',format='.0f')
        ]
    )

    points = line.mark_circle(
        size=110,
        color='#838F58'
    )

    labels = line.mark_text(
        dy=-18,
        color='#48533E',
        fontSize=13,
        fontWeight='normal'
    ).encode(
        text=alt.Text(f'{price_col}:Q', format='.0f')
    )

    chart = (line + points + labels).properties(height=320)

    st.altair_chart(chart, use_container_width=True)

    st.caption(
        'Показана средняя цена опубликованных тарифов '
        'аренды выбранного клуба в пересчёте на 60 минут. '
        'Состав тарифов между датами может различаться.'
    )
else:
    st.markdown('''
    <div style="
        background-color:#E8EDDF;
        border-left:3px solid #838F58;
        border-radius:12px;
        padding:18px 20px;
        color:#384331;
        margin:16px 0;
    ">
        Для выбранного клуба пока недостаточно истории.
        Нужны наблюдения минимум за две даты.
    </div>
    ''', unsafe_allow_html=True)

# =========================
# СРАВНЕНИЕ ДВУХ КЛУБОВ
# =========================

st.divider()
st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">05 / АНАЛИЗ</div>
    <h2>Сравнение двух клубов</h2>
</div>
''',unsafe_allow_html=True)

st.caption(
    'Сравнение средних опубликованных цен, '
    'ценового индекса и количества тарифов.'
)

club_options=list(clubs.keys())

if len(club_options)>=2:

    col1,col2=st.columns(2)

    with col1:
        club_a=st.selectbox(
            'Первый клуб',
            club_options,
            index=0,
            key='compare_club_a'
        )

    with col2:
        club_b=st.selectbox(
            'Второй клуб',
            club_options,
            index=1,
            key='compare_club_b'
        )

    if club_a==club_b:
        st.warning('Выберите два разных клуба.')

    else:
        stats_a=clubs[club_a]
        stats_b=clubs[club_b]

        comparison_rows=[
            {
                'Показатель':'Средняя цена, ₽',
                club_a:round(stats_a['average_price']),
                club_b:round(stats_b['average_price'])
            },
            {
                'Показатель':'Медианная цена, ₽',
                club_a:round(stats_a['median_price']),
                club_b:round(stats_b['median_price'])
            },
            {
                'Показатель':'Минимальный тариф, ₽',
                club_a:round(stats_a['min_price']),
                club_b:round(stats_b['min_price'])
            },
            {
                'Показатель':'Максимальный тариф, ₽',
                club_a:round(stats_a['max_price']),
                club_b:round(stats_b['max_price'])
            },
            {
                'Показатель':'Price Index',
                club_a:round(stats_a['price_index'],1),
                club_b:round(stats_b['price_index'],1)
            },
            {
                'Показатель':'Количество тарифов',
                club_a:stats_a['tariff_count'],
                club_b:stats_b['tariff_count']
            }
        ]

        st.dataframe(
            pd.DataFrame(comparison_rows),
            hide_index=True,
            use_container_width=True
        )

        difference=(
            stats_a['average_price']
            -stats_b['average_price']
        )

        if difference>0:
            message=(
                f'Средняя опубликованная цена клуба {club_a} '
                f'выше, чем у {club_b}, на {difference:.0f} ₽.'
            )

        elif difference<0:
            message=(
                f'Средняя опубликованная цена клуба {club_b} '
                f'выше, чем у {club_a}, на {abs(difference):.0f} ₽.'
            )

        else:
            message='Средние опубликованные цены двух клубов совпадают.'

        st.markdown(f'''
        <div style="
            background-color:#E8EDDF;
            border-left:3px solid #838F58;
            border-radius:12px;
            padding:18px 20px;
            color:#384331;
            margin:16px 0;
        ">
            {message}
        </div>
        ''',unsafe_allow_html=True)

        st.caption(
            'Сравниваются средние по опубликованным тарифам. '
            'Условия аренды и состав тарифов клубов могут различаться.'
        )

else:
    green_notice('Для сравнения необходимо минимум два клуба.')

# =========================
# СРАВНЕНИЕ ОДИНАКОВЫХ ТАРИФОВ
# =========================

import sqlite3
from db.connection import DB_PATH

st.divider()
st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">06 / АНАЛИЗ</div>
    <h2>Сравнение тарифов с одинаковыми условиями</h2>
</div>
''',unsafe_allow_html=True)

st.caption(
    'Сравниваются тарифы с одинаковым типом корта, '
    'днём недели, временем и длительностью аренды.'
)

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory=sqlite3.Row

    rows=conn.execute('''
        SELECT
            c.name AS club,
            t.product_type,
            t.days,
            t.start_time,
            t.end_time,
            t.duration_minutes,
            t.price
        FROM tariff t
        JOIN club c ON c.club_id=t.club_id
        JOIN service s ON s.service_id=t.service_id
        WHERE s.service_name='Аренда корта'
        AND t.checked_at=(
            SELECT MAX(t2.checked_at)
            FROM tariff t2
            WHERE t2.club_id=t.club_id
            AND t2.service_id=t.service_id
        )
    ''').fetchall()

tariff_data=[dict(row) for row in rows]

if len(club_options)>=2 and club_a!=club_b:

    first={
        (
            row['product_type'],
            row['days'],
            row['start_time'],
            row['end_time'],
            row['duration_minutes']
        ):row['price']
        for row in tariff_data
        if row['club']==club_a
    }

    second={
        (
            row['product_type'],
            row['days'],
            row['start_time'],
            row['end_time'],
            row['duration_minutes']
        ):row['price']
        for row in tariff_data
        if row['club']==club_b
    }

    matched=set(first)&set(second)

    comparison_rows=[]

    for key in sorted(matched):

        price_a=first[key]
        price_b=second[key]

        comparison_rows.append({
            'Тип корта':key[0],
            'День':key[1],
            'Время':f'{key[2]}–{key[3]}',
            'Длительность, мин':key[4],
            club_a:price_a,
            club_b:price_b,
            'Разница, ₽':price_a-price_b
        })

    if comparison_rows:

        st.dataframe(
            pd.DataFrame(comparison_rows),
            hide_index=True,
            use_container_width=True
        )

        st.caption(
            'Положительная разница означает, что первый клуб дороже. '
            'Отрицательная — что дешевле.'
        )

    else:
        green_notice(
            'У выбранных клубов нет тарифов с полностью '
            'совпадающими условиями аренды.'
        )

else:
    green_notice('Выберите два разных клуба выше.')

# =========================
# ИСТОРИЯ КОНКРЕТНОГО ТАРИФА
# =========================

st.divider()
st.markdown('''
<div class="analysis-section">
    <div class="analysis-section-label">07 / АНАЛИЗ</div>
    <h2>История конкретного тарифа</h2>
</div>
''',unsafe_allow_html=True)

st.caption(
    'Изменение стоимости одного и того же тарифа '
    'по датам наблюдений.'
)

tariff_history=get_all_court_tariffs_history()

tariff_clubs=sorted(set(
    row['club'] for row in tariff_history
))

selected_history_club=st.selectbox(
    'Клуб',
    tariff_clubs,
    key='tariff_history_club'
)

club_history=[
    row for row in tariff_history
    if row['club']==selected_history_club
]

def tariff_identity(row):
    return (
        row['product_type'],
        row['days'],
        row['start_time'],
        row['end_time'],
        row['duration_minutes']
    )

tariff_options={}

for row in club_history:
    key=tariff_identity(row)

    label=(
        f"{row['product_type']} | "
        f"{row['days']} | "
        f"{row['start_time']}–{row['end_time']} | "
        f"{row['duration_minutes']} мин"
    )

    tariff_options[label]=key

if tariff_options:

    selected_tariff=st.selectbox(
        'Тариф',
        sorted(tariff_options.keys()),
        key='selected_tariff_history'
    )

    selected_key=tariff_options[selected_tariff]

    tariff_points=[]

    for row in club_history:
        if tariff_identity(row)!=selected_key:
            continue

        tariff_points.append({
            'Дата':row['checked_at'],
            'Цена, ₽':row['price']
        })

    tariff_df=pd.DataFrame(tariff_points)

    tariff_df=tariff_df.drop_duplicates(
        subset=['Дата']
    ).sort_values('Дата')

    if len(tariff_df)>=2:

        st.line_chart(
            tariff_df.set_index('Дата'),
            color='#838F58'
        )

        first_price=tariff_df.iloc[0]['Цена, ₽']
        last_price=tariff_df.iloc[-1]['Цена, ₽']

        difference=last_price-first_price

        st.metric(
            'Изменение цены',
            f'{difference:+.0f} ₽'
        )

    else:
        green_notice(
            'Для этого тарифа пока есть только одно наблюдение.'
        )

else:
    green_notice('Для клуба пока нет истории тарифов.')


