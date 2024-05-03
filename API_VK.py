import subprocess

import vk_api

output = subprocess.check_output(["netsh", "wlan", "show", "interface"])

def parser(friends):
    array = []
    for friend in friends:
        fio = friend["first_name"] + " " + friend["last_name"]
        array.append(fio)
    return array


def get_friends(user_id, api_version, access_token):
    if "Подключено" in output.decode('cp866'):
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()

        response = vk.users.get(user_ids=user_id, v=api_version)
        user_info = response[0]
        id = user_info.get('id')

        response = vk.friends.get(user_id=id, fields='uid,first_name,last_name', v=api_version)

        friends = response['items']
        return friends
    else:
        return "You are not connected to WiFi."


api_version = '5.131'
user_id = 'chugunovets'
access_token = 'a9342782a9342782a9342782eeaa2c0f5daa934a9342782cf1b1ffdd7cf055c8ac204ef'

try:
    friends = get_friends(user_id, api_version, access_token)
    if friends == "You are not connected to WiFi.":
        print(friends)
    else:
        friends_fio = parser(friends)
        for friend_fio in friends_fio:
            print(friend_fio)
except vk_api.exceptions.ApiError as e:
    print(f"Failed to retrieve friends: {e}")
except IndexError as e:
    print("Error: List index is out of range, please check the response from the API")
