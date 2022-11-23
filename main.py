from flask import Flask, request, render_template
from sqlite3 import connect
import logging
from logging.handlers import RotatingFileHandler
from aiogram.types import ReplyKeyboardRemove
from threading import Timer
import config
import telegam_api
import yandex_maps_api

application = Flask(__name__)
file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 1024, backupCount=20)
file_handler.setLevel(logging.ERROR)
application.logger.setLevel(logging.ERROR)
application.logger.addHandler(file_handler)


def send_geo_error(user_id):
    con = connect('data/db.db')
    cur = con.cursor()
    mg = cur.execute(f"SELECT must_geo FROM users WHERE id == '{user_id}'").fetchone()[0]
    if not mg:
        return
    cur.execute(f"UPDATE users SET must_geo=0 WHERE id == '{user_id}'")
    con.commit()
    telegam_api.send_mess(user_id, config.send_geo_error_text, ReplyKeyboardRemove())
    telegam_api.send_site_inline_message(user_id)


@application.route(config.ssl_certification_url, methods=['GET'])
def ssl_certification():
    return config.ssl_certification_text, 200


@application.route('/telegram_web_geo/<int:user_id>', methods=['GET', 'POST'])
def index(user_id):
    if request.method == 'GET':
        return render_template('main.html', api_key=config.yandex_maps_api_key)
    con = connect('data/db.db')
    cur = con.cursor()
    data_ = cur.execute(f'SELECT * FROM users WHERE id == "{user_id}"').fetchone()
    if data_[1] == 3:
        data = request.json
        cur.execute(
            f'UPDATE users SET step=5, must_geo=0, place="{data["longitude"]},{data["latitude"]}" ' +
            f'WHERE id == "{user_id}"'
        )
        con.commit()
        yandex_maps_api.make_response(user_id)
    return {}, 200


@application.route('/telegram_bot', methods=['GET', 'POST'])
def bot():
    if 'message' not in request.json:
        return {}, 200

    message = request.json['message']
    user_id = message['chat']['id']
    con = connect('data/db.db')
    cur = con.cursor()

    if 'location' in message:
        data = cur.execute(f'SELECT * FROM users WHERE id == "{user_id}"').fetchone()
        if not data or data[1] != 3:
            telegam_api.send_mess(user_id, 'Не понял команды', '')
            return {}, 200
        longitude, latitude = message["longitude"]["longitude"], message["location"]["latitude"]
        cur.execute(
            f'UPDATE users SET step=4, must_geo=0, place="{longitude},{latitude}" WHERE id == "{user_id}"'
        )
        con.commit()
        telegam_api.send_mess(user_id, 'Геолокация определена верно?', config.true_false)
        return {}, 200

    if 'text' not in message:
        telegam_api.send_mess(user_id, 'Не понял команды', '')
        return {}, 200

    if message['text'] == '/start':
        data = cur.execute(f'SELECT * FROM users WHERE id == "{user_id}"').fetchone()
        if not data:
            cur.execute("INSERT INTO users (id) VALUES (?)", (user_id,))
            con.commit()
        telegam_api.send_mess(user_id, config.start_text, config.start_keys)

    elif message['text'] == 'Хочу узнать что вокруг':
        cur.execute(f"UPDATE users SET step=2 WHERE id == '{user_id}'")
        con.commit()
        telegam_api.send_mess(user_id, 'Вы хотите посмотреть рестораны вокруг? (или в другом месте)', config.true_false)

    elif message['text'] == 'Помощь':
        telegam_api.send_mess(user_id, config.help_text, config.start_keys)

    elif message['text'] == 'Да':
        data = cur.execute(f'SELECT * FROM users WHERE id == "{user_id}"').fetchone()
        if not data or data[1] == 2:
            cur.execute(f"UPDATE users SET step=3, must_geo=1 WHERE id == '{user_id}'")
            con.commit()
            Timer(10.0, send_geo_error, args=(user_id,)).start()
            telegam_api.send_mess(user_id, 'Отправьте нам ваши координаторы',
                                  config.location_keys)
        elif not data or data[1] == 4:
            cur.execute(f"UPDATE users SET step=1, must_geo=0 WHERE id == '{user_id}'")
            con.commit()
            yandex_maps_api.make_response(user_id)
        else:
            telegam_api.send_mess(user_id, 'Не понял команды', '')

    elif message['text'] == 'Нет':
        data = cur.execute(f'SELECT * FROM users WHERE id == "{user_id}"').fetchone()
        if not data or data[1] == 2 or data[1] == 4:
            cur.execute(f"UPDATE users SET step=3, must_geo=0 WHERE id == '{user_id}'")
            con.commit()
            if data and data[1] == 2:
                text_ = 'Укажите ваше местоположение на нашем сайте.'
            else:
                text_ = 'Жаль, давайте тогда попробуем указать ваше местоположение на нашем сайте'
            telegam_api.send_mess(user_id, text_, ReplyKeyboardRemove())
            telegam_api.send_site_inline_message(user_id)
        else:
            telegam_api.send_mess(user_id, 'Не понял команды', '')

    else:
        telegam_api.send_mess(user_id, 'Не понял команды', '')
    return {}, 200


@application.errorhandler(500)
def internal_error(exception):
    application.logger.error(exception)
    return {}, 200


if __name__ == '__main__':
    application.run(host='0.0.0.0')
