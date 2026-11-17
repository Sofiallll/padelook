import re

from parsers.padelgrad_parser import (
    URL,
    get_page_text,
    clean_price
)


def main():

    text=get_page_text(URL)

    start=text.find('Корт панорамный')
    end=text.find('Вводное занятие',start)

    print('Начало блока:',start)
    print('Конец блока:',end)

    if start==-1 or end==-1:
        print('Не удалось найти границы блока')
        return

    court_block=text[start:end]

    prices=re.findall(
        r'(\d[\d\s\xa0]*)\s*₽',
        court_block
    )

    print('\nКоличество найденных цен:',len(prices))

    print('\n--- СПИСОК ЦЕН ---')

    for i,price in enumerate(prices,1):
        print(i,clean_price(price))

    print('\n--- ПОЛНЫЙ ТЕКСТ БЛОКА ---')
    print(court_block)


if __name__=='__main__':
    main()