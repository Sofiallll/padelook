import pandas as pd
import streamlit as st

from analytics.competitors import (
    get_price_analytics,
    get_services_comparison,
    get_competitor_changes,
    get_weekly_insights
)


st.title('Конкуренты, цены и монетизация')

st.write(
    'Сравнение цен и предложений падел-клубов Санкт-Петербурга.'
)


# =========================
# ПОЛУЧАЕМ АНАЛИТИКУ
# =========================

price_data=get_price_analytics()
market=price_data['market']
clubs=price_data['clubs']


if not market:
    st.warning('В базе пока недостаточно данных для аналитики.')
    st.stop()


# =========================
# KPI РЫНКА
# =========================

st.subheader('Цены на аренду кортов')

col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric(
        'Средняя цена',
        f"{market['average_price']:.0f} ₽"
    )
    st.caption(
        'Средняя по опубликованным тарифам аренды '
        'с равным весом каждого клуба'
    )

with col2:
    st.metric(
        'Медианная цена',
        f"{market['median_price']:.0f} ₽"
    )
    st.caption(
        'Медиана клубных медиан'
    )

with col3:
    st.metric(
        'Минимальный тариф',
        f"{market['min_price']:.0f} ₽"
    )
    st.caption(
        'Минимальная опубликованная цена за 60 минут'
    )

with col4:
    st.metric(
        'Максимальный тариф',
        f"{market['max_price']:.0f} ₽"
    )
    st.caption(
        'Максимальная опубликованная цена за 60 минут'
    )


st.divider()


# =========================
# PRICE INDEX
# =========================

st.subheader('Price Index')

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


st.bar_chart(
    price_index_df,
    x='Клуб',
    y='Price Index'
)


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



# =========================
# ЛЕНТА ИЗМЕНЕНИЙ
# =========================

st.subheader('Лента изменений конкурентов')

st.caption(
    'Что изменилось между двумя последними проверками.'
)

changes=get_competitor_changes()


if not changes:

    st.info(
        'Пока недостаточно истории для сравнения. '
        'После следующего обновления данных здесь появятся '
        'изменения цен, новые тарифы и услуги.'
    )

else:

    for change in changes[:6]:

        if change['type']=='price_up':
            icon='🔴'

        elif change['type']=='price_down':
            icon='🟢'

        elif change['type']=='new_service':
            icon='🆕'

        elif change['type']=='new_tariff':
            icon='🆕'

        else:
            icon='⚪'

        with st.container(border=True):

            st.markdown(
                f"### {icon} {change['title']}"
            )

            st.write(
                change['description']
            )

            st.caption(
                f"Проверено: {change['date']}"
            )
st.divider()


# =========================
# АНАЛИТИЧЕСКИЙ ВЫВОД
# =========================

st.subheader('Аналитический вывод недели')

st.caption(
    'Автоматическая интерпретация обнаруженных изменений.'
)

insights=get_weekly_insights()

for insight in insights:

    if insight['level']=='warning':

        st.warning(
            f"**{insight['title']}**\n\n"
            f"{insight['text']}"
        )

    elif insight['level']=='success':

        st.success(
            f"**{insight['title']}**\n\n"
            f"{insight['text']}"
        )

    else:

        st.info(
            f"**{insight['title']}**\n\n"
            f"{insight['text']}"
        )


st.divider()
# =========================
# ВЫБОР КЛУБА
# =========================

st.subheader('Карточка клуба')


selected_club=st.selectbox(
    'Выберите клуб',
    list(clubs.keys())
)


club_stats=clubs[selected_club]


col1,col2,col3,col4=st.columns(4)


col1.metric(
    'Средняя цена',
    f"{club_stats['average_price']:.0f} ₽"
)

col2.metric(
    'Медианная цена',
    f"{club_stats['median_price']:.0f} ₽"
)

col3.metric(
    'Price Index',
    f"{club_stats['price_index']:.1f}"
)

col4.metric(
    'Количество тарифов',
    club_stats['tariff_count']
)


if club_stats['price_index']>100:

    difference=club_stats['price_index']-100

    st.info(
        f'Средняя цена по опубликованным тарифам клуба '
        f'примерно на {difference:.1f}% выше среднего '
        f'уровня рассматриваемого рынка.'
    )

elif club_stats['price_index']<100:

    difference=100-club_stats['price_index']

    st.info(
        f'Средняя цена по опубликованным тарифам клуба '
        f'примерно на {difference:.1f}% ниже среднего '
        f'уровня рассматриваемого рынка.'
    )

else:

    st.info(
        'Средняя цена клуба соответствует '
        'среднему уровню рассматриваемого рынка.'
    )


st.divider()


# =========================
# СРАВНЕНИЕ УСЛУГ
# =========================

st.subheader('Сравнение услуг')


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


st.dataframe(
    services_df,
    hide_index=True,
    use_container_width=True
)


st.caption(
    '«Нет данных» означает, что наличие или отсутствие услуги '
    'пока не подтверждено открытыми источниками.'
)
