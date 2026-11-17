import re
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

URL='https://padelstarclub.ru/spb/prices'
MAIN_URL='https://padelstarclub.ru/spb'


def clean_price(price):
    return int(
        price.replace(' ','').replace('\xa0','')
    )


def get_prices(block):
    prices=re.findall(
        r'(\d[\d\s\xa0]*)\s*₽',
        block
    )

    return [
        clean_price(price)
        for price in prices
    ]


def get_page_html(url):
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)

        page=browser.new_page()

        page.goto(
            url,
            wait_until='domcontentloaded',
            timeout=30000
        )

        page.wait_for_load_state('networkidle')

        html=page.content()

        browser.close()

        return html


def get_page_text(url):
    html=get_page_html(url)

    soup=BeautifulSoup(
        html,
        'html.parser'
    )

    text=' '.join(soup.stripped_strings)
    text=re.sub(r'\s+',' ',text).strip()

    return text


def parse_kult_padel():

    text=get_page_text(URL)

    tariffs=[]

    # =========================
    # 1. КОРТЫ PANORAMIC
    # =========================

    panoramic_start=text.find(
        'КОРТЫ PANORAMIC'
    )

    panoramic_end=text.find(
        'КОРТ ULTRA-PANORAMIC',
        panoramic_start
    )

    if panoramic_start==-1 or panoramic_end==-1:
        raise ValueError(
            'Не удалось найти блок тарифов Panoramic'
        )

    panoramic_block=text[
        panoramic_start:panoramic_end
    ]

    panoramic_prices=get_prices(
        panoramic_block
    )

    if len(panoramic_prices)!=4:
        raise ValueError(
            f'Ожидалось 4 цены Panoramic, найдено {len(panoramic_prices)}'
        )

    panoramic_tariffs=[
        (
            'Будни',
            '08:00',
            '11:00',
            panoramic_prices[0]
        ),
        (
            'Выходные',
            '08:00',
            '11:00',
            panoramic_prices[1]
        ),
        (
            'Будни',
            '11:00',
            '17:00',
            panoramic_prices[2]
        ),
        (
            'Будни',
            '17:00',
            '23:00',
            panoramic_prices[3]
        ),
        (
            'Выходные',
            '11:00',
            '23:00',
            panoramic_prices[3]
        )
    ]

    for days,start_time,end_time,price in panoramic_tariffs:

        tariffs.append({
            'service':'Аренда корта',
            'product_type':'Panoramic',
            'days':days,
            'start_time':start_time,
            'end_time':end_time,
            'price':price,
            'price_type':'Точная',
            'duration_minutes':60,
            'quantity':1,
            'payment_unit':'корт / 60 мин',
            'payment_mode':None,
            'tariff_type':'Обычный',
            'note':'На игру предоставляются 3 мяча'
        })

    # =========================
    # 2. КОРТЫ ULTRA-PANORAMIC
    # =========================

    ultra_start=text.find(
        'КОРТ ULTRA-PANORAMIC'
    )

    ultra_end=text.find(
        'Занятие с тренером',
        ultra_start
    )

    if ultra_start==-1 or ultra_end==-1:
        raise ValueError(
            'Не удалось найти блок тарифов Ultra-Panoramic'
        )

    ultra_block=text[
        ultra_start:ultra_end
    ]

    ultra_prices=get_prices(
        ultra_block
    )

    if len(ultra_prices)!=4:
        raise ValueError(
            f'Ожидалось 4 цены Ultra-Panoramic, найдено {len(ultra_prices)}'
        )

    ultra_tariffs=[
        (
            'Будни',
            '08:00',
            '11:00',
            ultra_prices[0]
        ),
        (
            'Выходные',
            '08:00',
            '11:00',
            ultra_prices[1]
        ),
        (
            'Будни',
            '11:00',
            '17:00',
            ultra_prices[2]
        ),
        (
            'Будни',
            '17:00',
            '23:00',
            ultra_prices[3]
        ),
        (
            'Выходные',
            '11:00',
            '23:00',
            ultra_prices[3]
        )
    ]

    for days,start_time,end_time,price in ultra_tariffs:

        tariffs.append({
            'service':'Аренда корта',
            'product_type':'Ultra-Panoramic',
            'days':days,
            'start_time':start_time,
            'end_time':end_time,
            'price':price,
            'price_type':'Точная',
            'duration_minutes':60,
            'quantity':1,
            'payment_unit':'корт / 60 мин',
            'payment_mode':None,
            'tariff_type':'Обычный',
            'note':'На игру предоставляются 3 мяча'
        })

    # =========================
    # 3. ИНДИВИДУАЛЬНЫЕ ТРЕНИРОВКИ
    # =========================

    trainer_start=text.find(
        'Занятие с тренером'
    )

    trainer_end=text.find(
        'Прокат инвентаря',
        trainer_start
    )

    if trainer_start==-1 or trainer_end==-1:
        raise ValueError(
            'Не удалось найти блок занятий с тренером'
        )

    trainer_block=text[
        trainer_start:trainer_end
    ]

    trainer_prices=get_prices(
        trainer_block
    )

    if len(trainer_prices)<3:
        raise ValueError(
            'Не удалось получить цены тренеров'
        )

    trainer_types=[
        (
            'Тренер',
            trainer_prices[0]
        ),
        (
            'Старший тренер',
            trainer_prices[1]
        ),
        (
            'Главный тренер',
            trainer_prices[2]
        )
    ]

    for trainer_type,price in trainer_types:

        tariffs.append({
            'service':'Индивидуальные тренировки',
            'product_type':trainer_type,
            'days':None,
            'start_time':None,
            'end_time':None,
            'price':price,
            'price_type':'Точная',
            'duration_minutes':60,
            'quantity':1,
            'payment_unit':'занятие',
            'payment_mode':'Корт оплачивается отдельно',
            'tariff_type':'Обычный',
            'note':'Каждый дополнительный участник +400 ₽'
        })

    # =========================
    # 4. ПРОКАТ ИНВЕНТАРЯ
    # =========================

    inventory_start=text.find(
        'Прокат инвентаря'
    )

    inventory_end=text.find(
        'Групповая тренировка',
        inventory_start
    )

    if inventory_start==-1 or inventory_end==-1:
        raise ValueError(
            'Не удалось найти блок проката инвентаря'
        )

    inventory_block=text[
        inventory_start:inventory_end
    ]

    inventory_prices=get_prices(
        inventory_block
    )

    if len(inventory_prices)!=5:
        raise ValueError(
            f'Ожидалось 5 цен инвентаря, найдено {len(inventory_prices)}'
        )

    inventory_tariffs=[
        (
            'Аренда ракеток',
            'Ракетка',
            inventory_prices[0],
            'за использование'
        ),
        (
            'Аренда ракеток',
            'Ракетка PROF',
            inventory_prices[1],
            'за использование'
        ),
        (
            'Аренда мячей',
            'Новые мячи, 3 шт.',
            inventory_prices[2],
            'за использование'
        ),
        (
            'Продажа инвентаря',
            'Новые мячи, 3 шт.',
            inventory_prices[3],
            'комплект'
        ),
        (
            'Аренда мячей',
            'Корзина мячей',
            inventory_prices[4],
            'за использование'
        )
    ]

    for service,product_type,price,payment_unit in inventory_tariffs:

        tariffs.append({
            'service':service,
            'product_type':product_type,
            'days':None,
            'start_time':None,
            'end_time':None,
            'price':price,
            'price_type':'Точная',
            'duration_minutes':None,
            'quantity':1,
            'payment_unit':payment_unit,
            'payment_mode':'Оплачивается отдельно',
            'tariff_type':'Обычный',
            'note':None
        })

    # =========================
    # 5. ГРУППОВЫЕ ТРЕНИРОВКИ
    # =========================

    group_start=text.find(
        'Групповая тренировка'
    )

    group_end=text.find(
        'Дополнительные услуги',
        group_start
    )

    if group_start==-1 or group_end==-1:
        raise ValueError(
            'Не удалось найти блок групповых тренировок'
        )

    group_block=text[
        group_start:group_end
    ]

    group_prices=get_prices(
        group_block
    )

    if len(group_prices)!=2:
        raise ValueError(
            f'Ожидалось 2 цены групповых тренировок, найдено {len(group_prices)}'
        )

    group_tariffs=[
        (
            'С тренером',
            group_prices[0]
        ),
        (
            'Со старшим тренером',
            group_prices[1]
        )
    ]

    for product_type,price in group_tariffs:

        tariffs.append({
            'service':'Групповые тренировки',
            'product_type':product_type,
            'days':None,
            'start_time':None,
            'end_time':None,
            'price':price,
            'price_type':'Точная',
            'duration_minutes':90,
            'quantity':1,
            'payment_unit':'занятие',
            'payment_mode':'Корт, тренер и инвентарь включены',
            'tariff_type':'Обычный',
            'note':None
        })

    # =========================
    # 6. ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ
    # =========================

    additional_start=text.find(
        'Дополнительные услуги'
    )

    additional_end=text.find(
        'Стоимость игры в падел',
        additional_start
    )

    if additional_start==-1 or additional_end==-1:
        raise ValueError(
            'Не удалось найти блок дополнительных услуг'
        )

    additional_block=text[
        additional_start:additional_end
    ]

    additional_prices=get_prices(
        additional_block
    )

    if len(additional_prices)!=4:
        raise ValueError(
            f'Ожидалось 4 цены дополнительных услуг, найдено {len(additional_prices)}'
        )

    additional_tariffs=[
        (
            'VIP-раздевалка, 1.5 часа',
            90,
            additional_prices[0]
        ),
        (
            'VIP-раздевалка, 2 часа',
            120,
            additional_prices[1]
        ),
        (
            'VIP-раздевалка, 2.5 часа',
            150,
            additional_prices[2]
        ),
        (
            'Переговорная комната, 1 час',
            60,
            additional_prices[3]
        )
    ]

    for product_type,duration,price in additional_tariffs:

        tariffs.append({
            'service':'Дополнительная услуга',
            'product_type':product_type,
            'days':None,
            'start_time':None,
            'end_time':None,
            'price':price,
            'price_type':'Точная',
            'duration_minutes':duration,
            'quantity':1,
            'payment_unit':'бронирование',
            'payment_mode':None,
            'tariff_type':'Обычный',
            'note':None
        })

    # =========================
    # 7. СОБИРАЕМ СПИСОК УСЛУГ
    # =========================

    services={}

    # Если по услуге нашли тариф,
    # значит услуга точно есть
    for tariff in tariffs:

        services[tariff['service']]={
            'service':tariff['service'],
            'source_url':URL,
            'availability_status':'Есть'
        }

    # =========================
    # 8. ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ
    #    С ОСНОВНОЙ СТРАНИЦЫ
    # =========================

    main_text=get_page_text(
        MAIN_URL
    )

    # -------------------------
    # Вводная тренировка
    # -------------------------

    if (
        'вводная тренировка' in main_text.lower()
        or
        'вводное занятие' in main_text.lower()
    ):

        services[
            'Вводная тренировка'
        ]={
            'service':'Вводная тренировка',
            'source_url':MAIN_URL,
            'availability_status':'Есть'
        }

    # -------------------------
    # Корпоративные мероприятия
    # -------------------------

    if 'корпоратив' in main_text.lower():

        services[
            'Корпоративные мероприятия'
        ]={
            'service':'Корпоративные мероприятия',
            'source_url':MAIN_URL,
            'availability_status':'Есть'
        }

    # -------------------------
    # Турниры / открытые игры
    # -------------------------

    if 'турнир' in main_text.lower():

        services[
            'Турниры / открытые игры'
        ]={
            'service':'Турниры / открытые игры',
            'source_url':MAIN_URL,
            'availability_status':'Есть'
        }

    return {
        'club':'Культ Падел',
        'url':URL,
        'tariffs':tariffs,
        'services':list(
            services.values()
        )
    }