import vk_api, random
token = "f9a38be71df81831bd854f44bf26613d5f91dd6edeec8164f45261f5def3aba84d019b14ef3b914c869a2"

vk = vk_api.VkApi(token=token)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":int(random.uniform(0, 1000000))})

def user_information(user_id):
    need_info = {
                'user_id': user_id,
                'fields': ['first_name'] 
                }
    return (vk.method('users.get', need_info))[0]

def my_anonim_friend(user_id, name):
    params = {
             'user_id': user_id,
             'q': name,
             'count': 1,
             'fields': ['photo_max_orig']
             }
    vk.method('users.search')