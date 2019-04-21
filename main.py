import vk_api
import random 
import string
from vk_api.longpoll import VkLongPoll, VkEventType
from key_words import *
token = "f9a38be71df81831bd854f44bf26613d5f91dd6edeec8164f45261f5def3aba84d019b14ef3b914c869a2"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)
bd = {}

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":int(random.uniform(0, 1000000))})

def user_information(user_id):
    need_info = {
                'user_id': user_id,
                'fields': ['first_name'] 
                }
    print(vk.method('users.get', need_info))

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        user_information(event.user_id)
        all_request = event.text.lower()
        all_request = all_request.translate(string.maketrans("",""), string.punctuation)
        #удаляет пунтуацию. требует теста
        request = all_request.split()
        print(request)
        response = []
        for word in request:
            if word in HELLO:
                response.append(random.choice(HELLO))
            if word == "пока":
                response.append("Пока")
            if len(response) == 0:
                response.append("Не понялa вашего ответа..")
            response = '. '.join(response) + '.'
            write_msg(event.user_id, response) 