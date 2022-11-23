import config
from requests import post, get
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Проверка на соответствие веб хуков и реального расположения бота
if post(f'https://api.telegram.org/bot{config.telegram_api_key}/getWebhookInfo').json()['result']['url'] != \
        f'https://{config.site_domain}/telegram_bot':
    post(f'https://api.telegram.org/bot{config.telegram_api_key}/setwebhook')
    get(f'https://api.telegram.org/bot{config.telegram_api_key}/setwebhook?' +
        f'url=https://{config.site_domain}/telegram_bot')


def send_mess(user_id, text, reply_markup=None):
    if reply_markup:
        post(f'https://api.telegram.org/bot{config.telegram_api_key}/sendMessage',
             data={'chat_id': user_id, 'text': text, 'reply_markup': str(reply_markup)})
    else:
        post(f'https://api.telegram.org/bot{config.telegram_api_key}/sendMessage',
             data={'chat_id': user_id, 'text': text})


def send_site_inline_message(user_id):
    send_mess(user_id, config.send_geo_error_button_text, InlineKeyboardMarkup().add(
        InlineKeyboardButton('Отправить локацию', url=f'https://{config.site_domain}/telegram_web_geo/{user_id}')))
