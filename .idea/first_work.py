'''Первая работа с FL'''

import requests
from bs4 import BeautifulSoup
import fake_useragent
import openpyxl
from openpyxl.styles import Font, NamedStyle, Side, Border
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36'}      #User_Agent генерируется, чтобы сайт понимал, что к ниму обращается человек, а не бот
HOST = 'https://lkg.ru/'
# user = fake_useragent.UserAgent().random            #Можно рандомной генерации User_Agent
#
# header = {
#     'user-agent': user
# }

def get_html(url, params=None):                                           # Функция проверяет отвечает ли сайт на наш запрос, и отдает резуьтат запроса назад в функцию, которая вызвала данную функцию - parse()
    d = requests.get(url, headers=HEADERS, params=params)                  # ....применяется если нет необходимости проходить авторизацию на сайте
    return d

def product_categories(html):
    soup = BeautifulSoup(html, 'html.parser')
    categories = soup.find_all('div', class_='item_block lg col-lg-20 col-md-4 col-xs-6')
    x = len(categories)
    return categories

# Пагинация, определение количества страниц
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paginationTo = soup.find('div', class_='sm-pagination')
    if paginationTo:
        paginationTo = soup.find('div', class_='sm-pagination')              # Если есть класс class_='nums'
        pagination = paginationTo.find_all('span')                     # ... то выбрать все ссылки с тэгом 'a'
        return int(pagination[-1].get_text())
    else:
        return 1


def parse():
    for URL in [
        'https://lkg.ru/cond/',
    ]:
        html = get_html(URL)                                        #Выбранный URL передается в функцию get_html()
        if html.status_code == 200:
            catalog = []
            # print(f'{html.text = }')
            categories_list = product_categories(html.text)
            for category in categories_list:
                inside_page_org = category.find('a').get('href'),              # Если необходимая информация по объекту содержится на вложенной странице, то необходимо перейти на эту html страницу
                inside_page = str(inside_page_org)[3:-3]                       # Используется при необходимости сделать срез строки (если в начале и в конце есть не неужные элементы)
                inside_page_href =str(HOST) + str(inside_page)                 # Определяю URL страницы на которую необхдимо перейти
                html_2 = get_html(inside_page_href)

                pages_count = get_pages_count(html_2.text)               # Сюда передается полученный html текст со страницы, полученный от функции get_pages_count

            for page in range (1, pages_count + 1):                  # после получения данных от функции пагинации, перебираем каждую страницу
                # print(f'Парсинг страницы {page} {pages_count} {URL}...')
                html = get_html(URL, params={'PAGEN_1': page})           # ... и парсим каждую страницу. 'PAGEN_1' - данное название надо смотреть в коде страницы, у каждого сайта оно может быть своё
                catalog.extend(get_content(html.text))                   # Сюда передается все данные с интернет страниц, для дальнейшей обработки html файла
                # time.sleep(1)                                            # Делаю паузу между запросами, чтобы сервер сайта, по частоте запросов не понимал, что к нему обращается парсер
            FILE = 'parseResult' + '.csv'
            save_file(catalog, FILE)


            print(f'Получено {len(catalog)} товаров')
        else:
            print('Error')

if __name__ == '__main__':
    parse()