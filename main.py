from services.update_service import update_padelgrad,update_kult_padel


def print_result(result):
    print('Клуб:',result['club'])
    print('Найдено услуг:',result['services_found'])
    print('Найдено тарифов:',result['found'])
    print('Добавлено тарифов:',result['added'])
    print('Пропущено тарифов:',result['skipped'])
    print()


def main():
    results=[
        update_padelgrad(),
        update_kult_padel()
    ]

    for result in results:
        print_result(result)


if __name__=='__main__':
    main()