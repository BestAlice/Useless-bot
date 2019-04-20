import vk_api
import random 
from vk_api.longpoll import VkLongPoll, VkEventType
from key_words import *
token = "f9a38be71df81831bd854f44bf26613d5f91dd6edeec8164f45261f5def3aba84d019b14ef3b914c869a2"

vk = vk_api.VkApi(token=token)

longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":int(random.uniform(0, 1000000))})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        all_request = event.text.lower()
        request = all_request.split()
        for word in request:
            if word in HELLO:
                write_msg(event.user_id, random.choice(HELLO))
            elif word == "пока":
                write_msg(event.user_id, "Пока")
            else:
                write_msg(event.user_id, "Не понялa вашего ответа...")