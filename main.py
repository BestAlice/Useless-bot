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
    wiki = False
    UserModel(db.get_connection()).init_table()
    user_model = UserModel(db.get_connection())
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            info = user_information(event.user_id)
            user = user_model.get(info['id'])
            # (id, user_id, Имя, id собеседника (0, если его нет))
            print(user)
            all_request = event.text.lower()
            all_request = "".join(l for l in all_request if l not in string.punctuation) 
            request = all_request.split()
            logging.debug('{} прислал сообщение {}'.format(info['first_name'], request))
            print(request)
            response = []
            if user[3] != 0:
                for word in STOP_DIALOG:
                    if word in all_request:
                        user_model.stop_dialog(user[0], user[3])
                        break
                else:
                    write_msg(user[3], event.text)
            else:
                if 'vk.com/' in event.text:
                    start = event.text.find('vk.com/') + 7
                    name = event.text[start:].split()[0]
                    print(name)
                    person_id = id_by_name(name)
                    if person_id == 'error':
                        write_msg(event.user_id, 'id не пренадлежит пользователю')
                    else:
                        info_2 = user_information(person_id)
                        user_2 = user_model.get(info_2['id'])
                        if user_2[3] != 0:
                            write_msg(event.user_id, 'Собеседник уже сосотоит в диалоге')
                        if user[3] != 0:
                            user_model.stop_dialog(event.user_id, user[3])
                        user_model.new_dialog(info['id'], info_2['id'])
                        write_msg(info['id'], 'Начат диалог')
                        write_msg(info_2['id'], 'Начат диалог')
                if wiki:
                    response.append('Вот что я нашёл: \n' + str(wikipedia.summary(event.text)))
                    wiki = False
                else:
                    for word in request:
                        if word in HELLO:
                            response.append(random.choice(HELLO) + ', ' + info['first_name'])
                        #if 'httpsvkcom' in word:
                        #    name = word[11:]
                        #    person_id = id_by_name(name)
                        #    print(person_id)
                        if word == "help":
                            keyboard_vk(event.user_id)
                            response.append("n_N")
                        if word == "погода":
                            weather_vk(event.user_id)
                            response.append(".^_^")
                        if word == "вики":
                            wiki = True
                            response.append("Введите запрос")
                        if word == "пока" and len(response) == 0:
                            response.append("Пока")
                            user_model.delete_user(event.user_id)
                            logging.info('Завершение диалога с {}(id={})'.format(info['first_name'], info['id']))
                        if len(response) == 0:
                            response.append("Не понялa вашего ответа..")
                response = map(lambda x: x[0].upper() + x[1:] + '. ', response)
                response = ''.join(response)
                write_msg(event.user_id, response) 


if __name__ == '__main__':
    main()