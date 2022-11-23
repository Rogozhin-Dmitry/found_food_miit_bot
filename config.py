from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

telegram_api_key = '5678349157:AAEh7Mf6bxbBUkPIwCuaTClkD_ExprlJQjc'
yandex_maps_api_key = 'ea2d8f7a-b625-40bd-9ca1-6083f9c70202'
yandex_maps_organizations_api_key = 'fb2f066c-ad5c-4dec-b075-386b3cd7f12b'
telegram_admin_password = 'dep39'
site_domain = 'miit.dmitry-rogozhin.online'
obl = {
    '0.004,0.004': '500 метров',
    '0.008,0.008': '1000 метров',
    '0.012,0.012': '1500 метров',
    '0.016,0.016': '2000 метров',
    '0.02,0.02': '2500 метров'
}
help_text = '''
Чтобы отправить геолокацию, следуй инструкции:
1)В нижней части экрана нажми на кнопку "Хочу узнать что вокруг"
2)Если вы хотите указать свое место положение - нажмите "Да", если хотите указать другую геолокацию - нажмите "Нет"
3)Если вы нажали "Да", далее нажмите на кнопку "Отправить свою локацию" -> "Да"
  Если телеграм правильно определил ваше местоположение, нажмите кнопку "Да" -> Готово!
4)Если вы нажали "Нет" или телеграм не смог корректно определить вашу геолокацию,
  Нажмите на кнопку "Отправить свою локацию" -> "Да" 
  Выберите на карте нужное место и нажмите на него -> Готово!
'''

ssl_certification_url = '/.well-known/pki-validation/9AAD5EBF0017B21C9692120858B53AA1.txt'
ssl_certification_text = '''7F103E7C733032ABC9F914CDB72D028EDC31DDF4F943FDED9B61EBCC8FB75CA9
comodoca.com
c051dc09a6cae16'''

start_keys = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Хочу узнать что вокруг')).add(KeyboardButton('Помощь'))
true_false = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Да')).add(KeyboardButton('Нет'))
location_keys = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton('Отправить свою локацию', request_location=True))

yandex_maps_api_search_text = 'text=%D0%BA%D0%B0%D1%84%D0%B5,%D1%80%D0%B5%D1%81%D1%82%D0%BE%D1%80%D0%B0%D0%BD%D1%8B' + \
                              ',%D0%BA%D0%BE%D1%84%D0%B5%D0%B9%D0%BD%D0%B8&'

send_geo_error_text = 'Наверное, вы заблокировали возможность получения геопозиции для Телеграм, давайте попробуем ' + \
                      'передать ваше местоположение через наш сайт.'
send_geo_error_button_text = 'При переходе на сайт просто зафиксируйте местоположение и закройте вкладку.'
start_text = 'Это бот, в котором вы можете узнать рестораны вокруг'
