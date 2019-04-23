import vk_api
import random, string
from vk_api.longpoll import VkLongPoll, VkEventType
from key_words import *
from bd_users import DB, UserModel
from vk_metods import *
import logging

token = "f9a38be71df81831bd854f44bf26613d5f91dd6edeec8164f45261f5def3aba84d019b14ef3b914c869a2"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
db = DB()
logging.basicConfig(filename='info.log', 
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


def main():
    UserModel(db.get_connection()).init_table()
    user_model = UserModel(db.get_connection())
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            info = user_information(event.user_id)
            user = user_model.get(info['id'])
            # (id, user_id, Имя, id собеседника(0, если его нет))
            print(user)
            all_request = event.text.lower()
            all_request = "".join(l for l in all_request if l not in string.punctuation) 
            request = all_request.split()
            logging.debug('{} прислал сообщение {}'.format(info['first_name'], request))
            print(request)
            response = []
            for word in request:
                if word in HELLO:
                    response.append(random.choice(HELLO) + ', ' + info['first_name'])
                if word == "пока" and len(response) == 0:
                    response.append("Пока")
                    user_model.delete_user(event.user_id)
                    logging.info('Завершение диалога с {}(id={})'.format(info['first_name'], info['id']))
                elif len(response) == 0:
                    response.append("Не понялa вашего ответа..")
            response = map(lambda x: x[0].upper() + x[1:] + '. ', response)
            response = ''.join(response)
            write_msg(event.user_id, response) 

if __name__ == '__main__':
    main()