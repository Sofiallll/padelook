from datetime import date
from db.connection import get_connection

from parsers.padelgrad_parser import parse_padelgrad
from parsers.kult_padel_parser import parse_kult_padel

from repositories.club_repository import get_club_id_by_name
from repositories.service_repository import get_service_id_by_name
from repositories.source_repository import (
    get_source_id_by_url,
    update_source_check
)
from repositories.tariff_repository import add_tariff
from repositories.club_service_repository import add_club_service


def find_error_url(error,source_urls,main_url):

    response=getattr(error,'response',None)

    if response is not None:

        response_url=getattr(response,'url',None)

        if response_url in source_urls:
            return response_url

    error_text=str(error)

    for url in source_urls:

        if url in error_text:
            return url

    return main_url


def update_club(parser, main_url, source_urls):

    # =========================
    # 1. ЗАПУСКАЕМ ПАРСЕР
    # =========================

    try:
        data = parser()

    except Exception as error:

        if isinstance(error, ValueError):
            status = 'parse_error'
        else:
            status = 'failed'

        failed_url = find_error_url(
            error,
            source_urls,
            main_url
        )

        try:
            update_source_check(
                url=failed_url,
                status=status,
                error=str(error)
            )

        except Exception as status_error:
            print(
                'Не удалось записать статус проверки:',
                status_error
            )

        raise

    # =========================
    # 2. ПРОВЕРЯЕМ ДАННЫЕ ИЗ ПАРСЕРА
    # =========================

    club_id = get_club_id_by_name(data['club'])

    if club_id is None:
        raise ValueError(
            f"Клуб '{data['club']}' не найден в БД"
        )

    checked_at = date.today().isoformat()

    tariff_source_id = get_source_id_by_url(data['url'])

    if tariff_source_id is None:
        raise ValueError(
            f"Источник '{data['url']}' не найден в БД"
        )

    # =========================
    # 3. ПОДГОТАВЛИВАЕМ УСЛУГИ
    # =========================

    services_to_save = []
    processed_services = set()

    for service in data.get('services', []):

        service_id = get_service_id_by_name(
            service['service']
        )

        if service_id is None:
            raise ValueError(
                f"Услуга '{service['service']}' не найдена в БД"
            )

        source_id = get_source_id_by_url(
            service['source_url']
        )

        if source_id is None:
            raise ValueError(
                f"Источник '{service['source_url']}' не найден в БД"
            )

        services_to_save.append({
            'service_id': service_id,
            'source_id': source_id,
            'availability_status': service['availability_status']
        })

        processed_services.add(service_id)

    # =========================
    # 4. ПОДГОТАВЛИВАЕМ ТАРИФЫ
    # =========================

    tariffs_to_save = []

    for tariff in data['tariffs']:

        service_id = get_service_id_by_name(
            tariff['service']
        )

        if service_id is None:
            raise ValueError(
                f"Услуга '{tariff['service']}' не найдена в БД"
            )

        tariffs_to_save.append({
            'service_id': service_id,
            'data': tariff
        })

    # =========================
    # 5. СОХРАНЯЕМ ВСЁ В ОДНОЙ ТРАНЗАКЦИИ
    # =========================

    added = 0
    skipped = 0

    conn = get_connection()

    try:
        with conn:

            # Сначала сохраняем услуги

            for service in services_to_save:

                add_club_service(
                    club_id=club_id,
                    service_id=service['service_id'],
                    source_id=service['source_id'],
                    checked_at=checked_at,
                    availability_status=service['availability_status'],
                    conn=conn
                )

            # Затем сохраняем тарифы

            for item in tariffs_to_save:

                service_id = item['service_id']
                tariff = item['data']

                # Если услуга ещё не была добавлена,
                # создаём для неё запись

                if service_id not in processed_services:

                    add_club_service(
                        club_id=club_id,
                        service_id=service_id,
                        source_id=tariff_source_id,
                        checked_at=checked_at,
                        availability_status='Есть',
                        conn=conn
                    )

                    processed_services.add(service_id)

                result = add_tariff(
                    club_id=club_id,
                    service_id=service_id,
                    source_id=tariff_source_id,
                    product_type=tariff['product_type'],
                    days=tariff['days'],
                    start_time=tariff['start_time'],
                    end_time=tariff['end_time'],
                    price=tariff['price'],
                    price_type=tariff['price_type'],
                    duration_minutes=tariff['duration_minutes'],
                    quantity=tariff['quantity'],
                    payment_unit=tariff['payment_unit'],
                    payment_mode=tariff['payment_mode'],
                    tariff_type=tariff['tariff_type'],
                    checked_at=checked_at,
                    note=tariff['note'],
                    conn=conn
                )

                if result:
                    added += 1
                else:
                    skipped += 1

    finally:
        conn.close()

    # =========================
    # 6. ЗАПИСЫВАЕМ УСПЕШНЫЕ ПРОВЕРКИ
    # =========================

    checked_urls = {data['url']}

    for service in data.get('services', []):

        if service.get('source_url'):
            checked_urls.add(service['source_url'])

    for url in checked_urls:

        update_source_check(
            url=url,
            status='success'
        )

    # =========================
    # 7. ВОЗВРАЩАЕМ РЕЗУЛЬТАТ
    # =========================

    return {
        'club': data['club'],
        'found': len(data['tariffs']),
        'services_found': len(data.get('services', [])),
        'added': added,
        'skipped': skipped
    }


# =========================
# ОБНОВЛЕНИЕ ПАДЕЛГРАДА
# =========================

def update_padelgrad():

    return update_club(
        parser=parse_padelgrad,
        main_url='https://padelgrad.club/price',
        source_urls=[
            'https://padelgrad.club/price',
            'https://padelgrad.club/tournaments',
            'https://padelgrad.club/corporate'
        ]
    )


# =========================
# ОБНОВЛЕНИЕ КУЛЬТ ПАДЕЛА
# =========================

def update_kult_padel():

    return update_club(
        parser=parse_kult_padel,
        main_url='https://padelstarclub.ru/spb/prices',
        source_urls=[
            'https://padelstarclub.ru/spb/prices',
            'https://padelstarclub.ru/spb'
        ]
    )