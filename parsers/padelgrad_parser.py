import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL='https://padelgrad.club/price'
TOURNAMENTS_URL='https://padelgrad.club/tournaments'
CORPORATE_URL='https://padelgrad.club/corporate'

COURT_TYPES=[
    'Panoramic',
    'Mondo'
]

PERIODS=[
    ('Будни','08:00','17:00'),
    ('Будни','17:00','21:00'),
    ('Будни','21:00','23:00'),
    ('Выходные и праздники','08:00','17:00'),
    ('Выходные и праздники','17:00','21:00'),
    ('Выходные и праздники','21:00','23:00')
]


def clean_price(price):
    return int(
        price.replace(' ','').replace('\xa0','')
    )


def get_page_text(url):
    headers={
        'User-Agent':'Mozilla/5.0'
    }

    response=requests.get(
        url,
        headers=headers,
        timeout=15
    )

    # Если обычный requests работает
    if response.status_code==200:

        soup=BeautifulSoup(
            response.text,
            'html.parser'
        )

        text=' '.join(soup.stripped_strings)
        text=re.sub(r'\s+',' ',text).strip()

        return text

    # Если сайт запрещает обычный запрос,
    # открываем страницу как браузер
    if response.status_code==403:

        with sync_playwright() as p:
            browser=p.chromium.launch(
                headless=True
            )

            page=browser.new_page()

            page.goto(
                url,
                wait_until='domcontentloaded',
                timeout=30000
            )

            html=page.content()

            browser.close()

        soup=BeautifulSoup(
            html,
            'html.parser'
        )

        text=' '.join(soup.stripped_strings)
        text=re.sub(r'\s+',' ',text).strip()

        return text

    # Для остальных ошибок
    response.raise_for_status()


def parse_padelgrad():
    text=get_page_text(URL)

    tariffs=[]

    # -------------------------
    # 1. Аренда кортов
    # -------------------------

    start = text.find('Корт панорамный')
    end = text.find('1-2 человека', start)

    if start==-1 or end==-1:
        raise ValueError(
            'Не удалось найти блок аренды кортов'
        )

    court_block=text[start:end]

    prices=re.findall(
        r'(\d[\d\s\xa0]*)\s*₽',
        court_block
    )

    prices=[
        clean_price(price)
        for price in prices
    ]

    if len(prices) != 12:
        raise ValueError(
            f'Ожидалось 12 цен аренды, найдено {len(prices)}'
        )

    for period_index,(days,start_time,end_time) in enumerate(PERIODS):

        for court_index,product_type in enumerate(COURT_TYPES):

            price_index=period_index*2+court_index

            tariffs.append({
                'service':'Аренда корта',
                'product_type':product_type,
                'days':days,
                'start_time':start_time,
                'end_time':end_time,
                'price':prices[price_index],
                'price_type':'Точная',
                'duration_minutes':60,
                'quantity':1,
                'payment_unit':'корт / 60 мин',
                'payment_mode':None,
                'tariff_type':'Обычный',
                'note':None
            })
    # -------------------------
    # 2. Вводная тренировка
    # -------------------------

    trainer_start=text.find(
        'Тренер *стоимость',
        end
    )

    if trainer_start==-1:
        raise ValueError(
            'Не удалось найти блок индивидуальных тренировок'
        )

    intro_block=text[end:trainer_start]

    intro_prices=re.findall(
        r'(\d[\d\s\xa0]*)\s*₽',
        intro_block
    )

    if len(intro_prices)!=2:
        raise ValueError(
            f'Ожидалось 2 цены вводного занятия, найдено {len(intro_prices)}'
        )

    intro_types=[
        '1-2 человека',
        '3-4 человека'
    ]

    for product_type,price in zip(intro_types,intro_prices):

        tariffs.append({
            'service':'Вводная тренировка',
            'product_type':product_type,
            'days':None,
            'start_time':None,
            'end_time':None,
            'price':clean_price(price),
            'price_type':'Точная',
            'duration_minutes':60,
            'quantity':1,
            'payment_unit':'занятие',
            'payment_mode':'Корт, тренер и инвентарь включены',
            'tariff_type':'Обычный',
            'note':None
        })
    # -------------------------
    # 3. Индивидуальные тренировки
    # -------------------------

    trainer_types=[
        ('Тренер','Тренер *стоимость'),
        ('Старший тренер','Старший тренер *стоимость'),
        ('Главный тренер','Главный тренер *стоимость')
    ]

    trainer_positions=[]

    for trainer_name,marker in trainer_types:

        position=text.find(
            marker,
            trainer_start
        )

        if position!=-1:
            trainer_positions.append(
                (trainer_name,position)
            )

    trainers_end=text.find(
        'В любое время',
        trainer_start
    )

    if trainers_end==-1:
        trainers_end=len(text)

    for i,(trainer_name,position) in enumerate(trainer_positions):

        if i<len(trainer_positions)-1:
            block_end=trainer_positions[i+1][1]
        else:
            block_end=trainers_end

        trainer_block=text[
            position:block_end
        ]

        trainer_prices=re.findall(
            r'(\d[\d\s\xa0]*)\s*₽\s*[\\/]\s*час',
            trainer_block
        )

        if trainer_prices:

            trainer_price=clean_price(
                trainer_prices[-1]
            )

            tariffs.append({
                'service':'Индивидуальные тренировки',
                'product_type':trainer_name,
                'days':None,
                'start_time':None,
                'end_time':None,
                'price':trainer_price,
                'price_type':'Точная',
                'duration_minutes':60,
                'quantity':1,
                'payment_unit':'занятие',
                'payment_mode':'Корт оплачивается отдельно',
                'tariff_type':'Обычный',
                'note':'Дополнительный игрок +600 ₽/час, до 4 человек'
            })

    # -------------------------
    # 4. Групповые тренировки
    # -------------------------

    group_start=text.find(
        'Взрослые Детские'
    )

    group_end=text.find(
        'Клубные часы',
        group_start
    )

    if group_start!=-1 and group_end!=-1:

        group_block=text[
            group_start:group_end
        ]

        group_prices=re.findall(
            r'(\d[\d\s\xa0]*)\s*₽',
            group_block
        )

        group_prices=[
            clean_price(price)
            for price in group_prices
        ]

        if len(group_prices)>=2:

            tariffs.append({
                'service':'Групповые тренировки',
                'product_type':'Взрослая группа',
                'days':None,
                'start_time':None,
                'end_time':None,
                'price':group_prices[0],
                'price_type':'Точная',
                'duration_minutes':90,
                'quantity':1,
                'payment_unit':'занятие',
                'payment_mode':None,
                'tariff_type':'Обычный',
                'note':'Группа до 4 человек'
            })

            tariffs.append({
                'service':'Детские падел-программы',
                'product_type':'Детская группа',
                'days':None,
                'start_time':None,
                'end_time':None,
                'price':group_prices[1],
                'price_type':'Точная',
                'duration_minutes':90,
                'quantity':1,
                'payment_unit':'занятие',
                'payment_mode':None,
                'tariff_type':'Обычный',
                'note':'Группа до 6 человек'
            })

    # =========================
    # 5. Услуги клуба
    # =========================

    services={}

    # Все услуги, у которых нашли тариф,
    # автоматически считаем существующими
    for tariff in tariffs:

        services[tariff['service']]={
            'service':tariff['service'],
            'source_url':URL,
            'availability_status':'Есть'
        }

    # -------------------------
    # Турниры / открытые игры
    # -------------------------

    tournaments_text=get_page_text(
        TOURNAMENTS_URL
    )

    if 'турнир' in tournaments_text.lower():

        services[
            'Турниры / открытые игры'
        ]={
            'service':'Турниры / открытые игры',
            'source_url':TOURNAMENTS_URL,
            'availability_status':'Есть'
        }

    # -------------------------
    # Корпоративные мероприятия
    # -------------------------

    corporate_text=get_page_text(
        CORPORATE_URL
    )

    if 'корпоратив' in corporate_text.lower():

        services[
            'Корпоративные мероприятия'
        ]={
            'service':'Корпоративные мероприятия',
            'source_url':CORPORATE_URL,
            'availability_status':'Есть'
        }

    return {
        'club':'Паделград',
        'url':URL,
        'tariffs':tariffs,
        'services':list(services.values())
    }