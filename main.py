import vk_api
import random, string
from vk_api.longpoll import VkLongPoll, VkEventType
from key_words import *
from bd_users import DB, UserModel
from vk_metods import *
from vk_api.utils import get_random_id
import wikipedia
import logging

token = "f9a38be71df81831bd854f44bf26613d5f91dd6edeec8164f45261f5def3aba84d019b14ef3b914c869a2"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
db = DB()
wikipedia.set_lang("RU")
logging.basicConfig(filename='info.log', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


def main():
    UserModel(db.get_connection()).init_table()
    user_model = UserModel(db.get_connection())
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            weather = False
            info = user_information(event.user_id)
            user = user_model.get(info['id'])
            # (id, user_id, Имя, id собеседника (0, если его нет), значение wiki 0 или 1)
            print(user)
            all_request = event.text.lower()
            all_request = "".join(l for l in all_request if l not in string.punctuation) 
            request = all_request.split()
            logging.info('{} прислал сообщение {}'.format(info['first_name'], request))
            print(request)
            response = []
            if 'vk.com/' in event.text:
                    start = event.text.find('vk.com/') + 7
                    print(event.text[start:])
                    name = event.text[start:].split()[0]
                    print(name)
                    person_id = id_by_name(name)
                    if person_id == 'error':
                        write_msg(event.user_id, 'id пренадлежит не пользователю')
                    else:
                        info_2 = user_information(person_id)
                        user_2 = user_model.get(info_2['id'])
                        if user_2[3] != 0:
                            write_msg(event.user_id, 'Собеседник уже сосотоит в диалоге')
                            continue
                        if user[3] != 0:
                            user_model.stop_dialog(event.user_id, user[3])
                            write_msg(info['id'], 'Диалог завершён')
                            write_msg(user[3], 'Диалог завершён')
                        user_model.new_dialog(info['id'], info_2['id'])
                        write_msg(info['id'], 'Начат диалог')
                        write_msg(info_2['id'], 'Начат диалог')
                        continue
            elif user[3] != 0:
                info_2 = user_information(user[3])
                user_2 = user_model.get(info_2['id'])
                for word in STOP_DIALOG:
                    if word in all_request:
                        user_model.stop_dialog(user[1], user[3])
                        write_msg(info['id'], 'Диалог завершён')
                        write_msg(user[3], 'Диалог завершён')
                        break
                else:
                    write_msg(user[3], event.text)
                    logging.info('{} получил сообщение от {}'.format(info_2['first_name'] + ' ' + info_2['last_name'],
                                                                     info['first_name'] + ' ' + info['last_name']))
            else:
                if user[4]:  # значение wiki 0 или 1
                    try:
                        write_msg(event.user_id,'Вот что я нашёл: \n' + str(wikipedia.summary(event.text)))
                        wiki = False
                    except:
                        write_msg(event.user_id,'По запросу ничего не найдено')
                    user_model.wiki(info['id'], 0)
                    continue
                for word in request:
                    if word in HELLO:
                        response.append(random.choice(HELLO) + ', ' + info['first_name'])
                    if word == "клава":
                        keyboard_vk(event.user_id)
                        response.append("..")
                    if word in HELP:
                        keyboard_vk(event.user_id)
                        helps = open('help.txt', 'r')
                        stroka = ''
                        for st in  helps.readlines():
                            stroka += st[:-1]
                        response.append(stroka)
                        helps.close()
                    if weather:
                        weather_vk(event.user_id, word)
                        response.append(".^_^")
                        weather =False
                    if word == "погода":
                        weather = True
                        continue
                    if word == "вики":
                        user_model.wiki(info['id'], 1)
                        response.append("Введите запрос")
                    if word == 'спасибо':
                        response.append("Пожалуйста")
                    if (word == "пока" or word == "прощай") and len(response) == 0:
                        response.append("Пока. Надеюсь больше тебя не услышу")
                        if user[3] != 0:
                            user_model.wiki(user[3], 0)
                            write_msg(user[3], 'Собеседник самовыпилился. Приносим его извинения')
                        user_model.delete_user(event.user_id)
                        logging.info('Завершение диалога с {}(id={})'.format(info['first_name'], info['id']))
                    if len(response) == 0:
                        response.append("Не понялa вашего ответа..")
                if weather:
                    weather_vk(event.user_id)
                    response.append(".^_^")
                weather =False
                response = map(lambda x: x[0].upper() + x[1:] + '. ', response)
                response = ''.join(response)
                write_msg(event.user_id, response) 


if __name__ == '__main__':
    main()