from telegam_api import send_mess
import config
from requests import get
from sqlite3 import connect
from aiogram.types import ReplyKeyboardRemove


def make_response(user_id):
    send_mess(user_id, 'Отлично, мы получили ваши координаты. Уже ищем рестораны вокруг......',
              str(ReplyKeyboardRemove()))
    con = connect('data/db.db')
    cur = con.cursor()
    cords = cur.execute(f"SELECT place FROM users WHERE id == '{user_id}'").fetchone()[0]
    mess_text = ''
    for size in sorted(config.obl.keys(), key=lambda x: float(x.split(',')[0])):
        data = get(
            f'https://search-maps.yandex.ru/v1/?apikey={config.yandex_maps_organizations_api_key}&' +
            config.yandex_maps_api_search_text + 'type=biz&lang=ru_RU&results=24&ll=' + cords + '&spn=' + str(size)
        ).json()
        mess_text += f'На расстоянии в {config.obl[size]} мы нашли ' + str(
            data['properties']['ResponseMetaData']['SearchResponse']['found']) + ' заведений\n\n'
        for place in data['features']:
            if place['properties']['name'] in mess_text:
                continue
            mess_text += 'Название ' + place['properties']['name'] + '\n'
            if 'address' in place['properties']['CompanyMetaData']:
                mess_text += 'Адрес ' + place['properties']['CompanyMetaData']['address'] + '\n'
            elif 'description' in place['properties']:
                mess_text += 'Адрес ' + place['properties']['description'] + '\n'
            if 'url' in place['properties']['CompanyMetaData']:
                mess_text += 'Веб сайт ' + place['properties']['CompanyMetaData']['url'] + '\n'
            if 'Categories' in place['properties']['CompanyMetaData']:
                if place['properties']['CompanyMetaData']['Categories']:
                    mess_text += 'Категории: '
                    for category in place['properties']['CompanyMetaData']['Categories']:
                        mess_text += category['name'] + ', '
                    mess_text = mess_text[:-2]
                    mess_text += '\n'
            if 'Phones' in place['properties']['CompanyMetaData']:
                if place['properties']['CompanyMetaData']['Categories']:
                    mess_text += 'Телефон: '
                    for telephone in place['properties']['CompanyMetaData']['Phones']:
                        mess_text += telephone['formatted'] + ' '
                    mess_text = mess_text[:-1]
                    mess_text += '\n'
            try:
                if 'Hours' in place['properties']['CompanyMetaData']:
                    send_mess(user_id, str(place['properties']['CompanyMetaData']['Hours']['text']))
                    mess_text += 'Часы работы: ' + place['properties']['CompanyMetaData']['Hours']['text']
            except Exception as e:
                print(e)
            mess_text += '\n\n'
        if data['properties']['ResponseMetaData']['SearchResponse']['found'] >= 4:
            send_mess(user_id, mess_text, config.start_keys)
            return
        else:
            send_mess(user_id, 'Мы нашли очень мало заведений :(, увеличиваем область и ищем лучше',
                      ReplyKeyboardRemove())
    send_mess(user_id, 'Мы так и не нашли достаточно заведений :(, попробуйте поменять место поиска', config.start_keys)
    send_mess(user_id, mess_text, ReplyKeyboardRemove())
