import vk_api, random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import yandex_weather_api
import requests as req
from key_words import *

token = "f9a38be71df81831bd854f44bf26613d5f91dd6edeec8164f45261f5def3aba84d019b14ef3b914c869a2"

vk = vk_api.VkApi(token=token)

def write_msg(user_id, message):
    try:
        vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":int(random.uniform(0, 1000000))})
    except:
        print('Ошибка отправки сообщения')

def user_information(user_id):
    need_info = {
                'user_id': user_id,
                'fields': ['first_name',  'can_write_private_message']
                }
    return (vk.method('users.get', need_info))[0]

def id_by_name(name):
    this_id = vk.method('utils.resolveScreenName', {'screen_name': name})
    return this_id['object_id'] if this_id['type'] == 'user' else 'error'

def keyboard_vk(user_id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('help', color=VkKeyboardColor.DEFAULT)
    keyboard.add_button('погода', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('вики', color=VkKeyboardColor.NEGATIVE)
    vk.method('messages.send', {'user_id': user_id,
        'keyboard':keyboard.get_keyboard(),
        'message':'Вот команды',
        "random_id":int(random.uniform(0, 1000000))})

def weather_vk(user_id):
    response = None
    response = yandex_weather_api.get(req, "68d3b400-9852-4e39-9647-9606c25307ab", lat=32.045251, lon=54.782635, lang="ru_RU")
    #print(response) json файл чтобы прочитать по человечески http://jsonparseronline.com
    temp = response["fact"]["temp"]
    feels_like = response["fact"]["feels_like"]
    condition = response["fact"]["condition"]
    text_temp = "Температура " + str(temp) + ', '
    text_feels_like = "Чувствуется как " + str(feels_like) + ', '
    for word in SL_WEATHER:
        if condition == word:
            condition_ru = SL_WEATHER[word]
    vk.method('messages.send', {'user_id':user_id, 
                                'message':'Яндекс Погода сообщает:' + text_temp + text_feels_like + condition_ru, 
                                "random_id":int(random.uniform(0, 1000000))})