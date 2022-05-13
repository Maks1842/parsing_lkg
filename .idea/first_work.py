'''Первая работа с FL'''
import time

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
    return categories

# Пагинация, определение количества страниц
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paginationTo = soup.find('div', class_='nums')
    category_file_name = soup.find('div', class_='topic h1-global-block').find('h1').text
    if paginationTo:
        paginationTo = soup.find('div', class_='nums')              # Если есть класс class_='nums'
        pagination = paginationTo.find_all('a', class_='dark_link')[2].text
        return int(pagination), category_file_name
    else:
        return 1, category_file_name

def get_content(html):             # Функция принимает данные со страниц, согласно пагинации, на обработку. И далее из документа html, извлекается необходимая информация
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='col-lg-3 col-md-4 col-sm-6 col-xs-6 col-xxs-12 item item-parent item_block')

    catalog = []
    for item in items:
        category = ''
        name = ''
        model = ''
        art = ''
        description = ''
        inside_page_org = item.find('a').get('href'),              # Если необходимая информация по объекту содержится на вложенной странице, то необходимо перейти на эту html страницу
        inside_page = str(inside_page_org)[3:-3]               # Используется при необходимости сделать срез строки (если в начале и в конце есть не неужные элементы)
        inside_page_href =str(HOST) + str(inside_page)
        html_2 = get_html(inside_page_href)


        soup_2 = BeautifulSoup(html_2.text, 'html.parser')
        category = soup_2.find('div', id='bx_breadcrumb_1').find('span').text
        name = soup_2.find('h1', id='pagetitle').text
        print(f'{name}')
        model = soup_2.find('h1', id='pagetitle').text
        try:
            art = soup_2.find('span', itemprop='sku').text
        except Exception:
            art = ''
        description = soup_2.find('div', class_='tab-content').find_all('p')[0].text.strip()
        if 'additionalProperty' in soup_2:
            specifications = soup_2.find_all('tr', itemprop='additionalProperty')
            for parameter in specifications:
                type_indoor_unit = ''
                producer = ''
                inverter = ''
                serviced_area = ''
                energy_consumption_class = ''
                power_cooling_mode = ''
                power_consumption_cooling = ''
                power_heating_mode = ''
                power_consumption_heating = ''
                noise_level = ''
                maximum_length_communications = ''
                maximum_height_difference = ''
                maximum_airflow = ''
                refrigerant = ''
                phase = ''
                modes = ''
                speed_adjustment = ''
                additional_modes = ''
                other_functions = ''
                additional_information = ''
                dimensions_indoor_unit = ''
                dimensions_outdoor_unit = ''
                weight_indoor_unit = ''
                weight_outdoor_unit = ''
                control = ''
                image_1 = ''
                image_2 = ''

                if 'Тип внутреннего блока' in parameter.find('span', itemprop='name').text.strip():
                    type_indoor_unit = parameter.find('span', itemprop='value').text[1:-1].strip()
                elif 'Инвертор' in parameter.find('span', itemprop='name').text.strip():
                    inverter = parameter.find('span', itemprop='value').text.strip()
                elif 'Обслуживаемая площадь' in parameter.find('span', itemprop='name').text.strip():
                    serviced_area = parameter.find('span', itemprop='value').text.strip()
                elif 'Класс энергопотребления' in parameter.find('span', itemprop='name').text.strip():
                    energy_consumption_class = parameter.find('span', itemprop='value').text.strip()
                elif 'Мощность в режиме охлаждения,' in parameter.find('span', itemprop='name').text.strip():
                    power_cooling_mode = parameter.find('span', itemprop='value').text.strip()
                elif 'Потребляемая мощность при охлаждении' in parameter.find('span', itemprop='name').text.strip():
                    power_consumption_cooling = parameter.find('span', itemprop='value').text.strip()
                elif 'Мощность в режиме обогрева' in parameter.find('span', itemprop='name').text.strip():
                    power_heating_mode = parameter.find('span', itemprop='value').text.strip()
                elif 'Потребляемая мощность при обогреве' in parameter.find('span', itemprop='name').text.strip():
                    power_consumption_heating = parameter.find('span', itemprop='value').text.strip()
                elif 'Уровень шума' in parameter.find('span', itemprop='name').text.strip():
                    noise_level = parameter.find('span', itemprop='value').text.strip()
                elif 'Максимальная длина коммуникаций' in parameter.find('span', itemprop='name').text.strip():
                    maximum_length_communications = parameter.find('span', itemprop='value').text.strip()
                elif 'Максимальный перепад высот' in parameter.find('span', itemprop='name').text.strip():
                    maximum_height_difference = parameter.find('span', itemprop='value').text.strip()
                elif 'Максимальный воздушный поток' in parameter.find('span', itemprop='name').text.strip():
                    maximum_airflow = parameter.find('span', itemprop='value').text.strip()
                elif 'Тип хладагента' in parameter.find('span', itemprop='name').text.strip():
                    refrigerant = parameter.find('span', itemprop='value').text.strip()
                elif 'Фаза' in parameter.find('span', itemprop='name').text.strip():
                    phase = parameter.find('span', itemprop='value').text.strip()
                elif 'Основные режимы' in parameter.find('span', itemprop='name').text.strip():
                    modes = parameter.find('span', itemprop='value').text.strip()
                elif 'Регулировка скорости' in parameter.find('span', itemprop='name').text.strip():
                    speed_adjustment = parameter.find('span', itemprop='value').text.strip()
                elif 'Дополнительные режимы' in parameter.find('span', itemprop='name').text.strip():
                    additional_modes = parameter.find('span', itemprop='value').text.strip()
                elif 'Другие функции и особенности' in parameter.find('span', itemprop='name').text.strip():
                    other_functions = parameter.find('span', itemprop='value').text.strip()
                elif 'Дополнительная информация' in parameter.find('span', itemprop='name').text.strip():
                    additional_information = parameter.find('span', itemprop='value').text.strip()
                elif 'Габариты внутреннего блока' in parameter.find('span', itemprop='name').text.strip():
                    dimensions_indoor_unit = parameter.find('span', itemprop='value').text.strip()
                elif 'Габариты наружного блока' in parameter.find('span', itemprop='name').text.strip():
                    dimensions_outdoor_unit = parameter.find('span', itemprop='value').text.strip()
                elif 'Вес внутреннего блока' in parameter.find('span', itemprop='name').text.strip():
                    weight_indoor_unit = parameter.find('span', itemprop='value').text.strip()
                elif 'Вес внешнего блока' in parameter.find('span', itemprop='name').text.strip():
                    weight_outdoor_unit = parameter.find('span', itemprop='value').text.strip()
                elif 'Производитель' in parameter.find('span', itemprop='name').text.strip():
                    producer = parameter.find('span', itemprop='value').text.strip()

                elif 'Управление' in parameter.find('span', itemprop='name').text.strip():
                    control = parameter.find('span', itemprop='value').text.strip()
        else:
            type_indoor_unit = ''
            producer = ''
            inverter = ''
            serviced_area = ''
            energy_consumption_class = ''
            power_cooling_mode = ''
            power_consumption_cooling = ''
            power_heating_mode = ''
            power_consumption_heating = ''
            noise_level = ''
            maximum_length_communications = ''
            maximum_height_difference = ''
            maximum_airflow = ''
            refrigerant = ''
            phase = ''
            modes = ''
            speed_adjustment = ''
            additional_modes = ''
            other_functions = ''
            additional_information = ''
            dimensions_indoor_unit = ''
            dimensions_outdoor_unit = ''
            weight_indoor_unit = ''
            weight_outdoor_unit = ''
            control = ''
            image_1 = ''
            image_2 = ''



        # energy_consumption_class = soup_2.find_all('tr', itemprop='additionalProperty')[2].find('span', itemprop='value').text.strip()
        # power_cooling_mode = soup_2.find_all('tr', itemprop='additionalProperty')[3].find('span', itemprop='value').text.strip()
        # power_consumption_cooling = soup_2.find_all('tr', itemprop='additionalProperty')[4].find('span', itemprop='value').text.strip()
        # power_heating_mode = soup_2.find_all('tr', itemprop='additionalProperty')[5].find('span', itemprop='value').text.strip()
        # power_consumption_heating = soup_2.find_all('tr', itemprop='additionalProperty')[6].find('span', itemprop='value').text.strip()
        # noise_level = soup_2.find_all('tr', itemprop='additionalProperty')[7].find('span', itemprop='value').text.strip()
        # maximum_length_communications = soup_2.find_all('tr', itemprop='additionalProperty')[8].find('span', itemprop='value').text.strip()
        # maximum_height_difference = soup_2.find_all('tr', itemprop='additionalProperty')[9].find('span', itemprop='value').text.strip()
        # maximum_airflow = soup_2.find_all('tr', itemprop='additionalProperty')[10].find('span', itemprop='value').text.strip()
        # refrigerant = soup_2.find_all('tr', itemprop='additionalProperty')[11].find('span', itemprop='value').text.strip()
        # phase = soup_2.find_all('tr', itemprop='additionalProperty')[12].find('span', itemprop='value').text.strip()
        # modes = soup_2.find_all('tr', itemprop='additionalProperty')[13].find('span', itemprop='value').text.strip()
        # speed_adjustment = soup_2.find_all('tr', itemprop='additionalProperty')[14].find('span', itemprop='value').text.strip()
        # additional_modes = soup_2.find_all('tr', itemprop='additionalProperty')[15].find('span', itemprop='value').text.strip()
        # additional_information = soup_2.find_all('tr', itemprop='additionalProperty')[16].find('span', itemprop='value').text.strip()
        # dimensions_indoor_unit = soup_2.find_all('tr', itemprop='additionalProperty')[17].find('span', itemprop='value').text.strip()
        # dimensions_outdoor_unit = soup_2.find_all('tr', itemprop='additionalProperty')[18].find('span', itemprop='value').text.strip()
        # weight_indoor_unit =  soup_2.find_all('tr', itemprop='additionalProperty')[19].find('span', itemprop='value').text.strip()
        # weight_outdoor_unit = soup_2.find_all('tr', itemprop='additionalProperty')[20].find('span', itemprop='value').text.strip()
        # producer = soup_2.find_all('tr', itemprop='additionalProperty')[22].find('span', itemprop='value').text.strip()
        # type_indoor_unit = soup_2.find_all('tr', itemprop='additionalProperty')[23].find('span', itemprop='value').text[1:-1].strip()  # [1:-1] - удаляет ненужные символы спереди и сзади, strip() - удаляет лишние пробелы
        # try:
        #     control = soup_2.find_all('tr', itemprop='additionalProperty')[24].find('span', itemprop='value').text.strip()
        # except Exception:
        #     control = ''
            image_1_URL = soup_2.find('div', id='photo-0').find('a').get('href')
            image_1 = str(HOST) + str(image_1_URL)
            # image_2_URL = soup_2.find('div', id='photo-2').find('a').get('href')
            # image_2 = str(HOST) + str(image_2_URL)



        catalog.append({
            'Категория': category,
            'Тип внутреннего блока': type_indoor_unit,
            'Наименование': name,
            'Производитель': producer,
            'Наименование модели': model,
            'Артикул': art,
            'Описание': description,
            'Инвертор': inverter,
            'Обслуживаемая площадь, м²': serviced_area,
            'Класс энергопотребления': energy_consumption_class,
            'Мощность в режиме охлаждения, Вт': power_cooling_mode,
            'Потребляемая мощность при охлаждении, Вт': power_consumption_cooling,
            'Мощность в режиме обогрева, Вт': power_heating_mode,
            'Потребляемая мощность при обогреве, Вт': power_consumption_heating,
            'Уровень шума (мин/макс), дБ': noise_level,
            'Максимальная длина коммуникаций, м': maximum_length_communications,
            'Максимальный перепад высот, м': maximum_height_difference,
            'Максимальный воздушный поток, м3/мин': maximum_airflow,
            'Тип хладагента': refrigerant,
            'Фаза': phase,
            'Основные режимы': modes,
            'Регулировка скорости вращения вентилятора': speed_adjustment,
            'Дополнительные режимы': additional_modes,
            'Другие функции и особенности': other_functions,
            'Дополнительная информация': additional_information,
            'Габариты внутреннего блока (ШxВxГ), см': dimensions_indoor_unit,
            'Габариты наружного блока (ШxВxГ), см': dimensions_outdoor_unit,
            'Вес внутреннего блока, кг': weight_indoor_unit,
            'Вес внешнего блока, кг': weight_outdoor_unit,
            'Управление': control,
            'Фото1': image_1,
            'Фото2': image_2
        })
        time.sleep(2)
    return catalog

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
                url_page_href = str(HOST) + str(inside_page)                 # Определяю URL страницы на которую необхдимо перейти
                html_2 = get_html(url_page_href)
                value_pages_count = get_pages_count(html_2.text)
                pages_count = value_pages_count[0]
                file_name  = value_pages_count[1]

                for page in range (1, pages_count + 1):                  # после получения данных от функции пагинации, перебираем каждую страницу
                    print(f'Парсинг страницы {page}')
                    url_page_content = f'{url_page_href}?PAGEN_1={page}'                # Определяю URL страницы на которую необхдимо перейти
                    html_3 = get_html(url_page_content)           # ... и парсим каждую страницу. 'PAGEN_1' - данное название надо смотреть в коде или URL страницы, у каждого сайта оно может быть своё
                    catalog.extend(get_content(html_3.text))                   # Сюда передается все данные с интернет страниц, для дальнейшей обработки html файла
                    # time.sleep(1)                                            # Делаю паузу между запросами, чтобы сервер сайта, по частоте запросов не понимал, что к нему обращается парсер
                FILE = f'data/{file_name}.csv'
                save_file(catalog, FILE)


                print(f'{file_name}. Получено {len(catalog)} товаров')
        else:
            print('Error')

if __name__ == '__main__':
    parse()