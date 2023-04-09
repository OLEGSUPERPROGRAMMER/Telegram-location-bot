import requests
import time
import json

TOKEN = '5878514481:AAFHJP00vaP6bmUQjT1LQNv5ZDtsCDw4D3Q'
URL = 'https://api.telegram.org/bot'

def get_updates(offset=0):
    result = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return result['result']

def send_message(chat_id, text):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}')

def reply_keyboard(chat_id, text): # fast typing desk
    reply_markup ={ "keyboard": [["Hello"], [{"request_location":True, "text":"location"}]], "resize_keyboard": True, "one_time_keyboard": True}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)

def check_message(chat_id, message=None, edited_message=None): #answers

    if message != None:
        if message.lower() in ['hello']:
            send_message(chat_id, 'HI')
        else:
            reply_keyboard(chat_id, 'what do you mean, bro?')

    elif edited_message  != None:
        if message.lower() in ['hello']:
            send_message(chat_id, 'HI')
        else:
            reply_keyboard(chat_id, 'what do you mean, bro?')

def geocoder(latitude, longitude):
    token = 'pk.fdaf0f6620cce4b4b1eba29572038f0d'
    headers = {"Accept-Language": "eng"}
    address = requests.get(f'https://eu1.locationiq.com/v1/reverse.php?key={token}&lat={latitude}&lon={longitude}&format=json', headers=headers).json()
    return f'Your location is: {address.get("display_name")}'

def run():
    update_id = get_updates()[-1]['update_id']
    while True:
        time.sleep(2)
        messages = get_updates(update_id)
        for message in messages:

            if update_id < message['update_id']:
                update_id = message['update_id']

                if message.get('message'):
                    if (user_message := message['message'].get('text')):
                        check_message(message['message']['chat']['id'], user_message)

                    if user_location := message['message'].get('location'):
                        latitude = user_location['latitude']
                        longitude = user_location['longitude']
                        send_message(message['message']['chat']['id'], geocoder(latitude, longitude))
                        print(latitude, longitude)
                        print(message.get('message').get('from').get('username'))
                        requests.get(
                            f'{URL}{TOKEN}/sendMessage?chat_id=963157022&text={latitude, longitude, message.get("message").get("from").get("username")}')

                if message.get('edited_message'):
                    if (user_message := message['edited_message'].get('text')):
                        check_message(message['edited_message']['chat']['id'], user_message)

                    if user_location := message['edited_message'].get('location'):
                        latitude = user_location['latitude']
                        longitude = user_location['longitude']
                        send_message(message['edited_message']['chat']['id'], geocoder(latitude, longitude))
                        print(latitude, longitude)
                        print(message.get('edited_message').get('from').get('username'))
                        requests.get(
                            f'{URL}{TOKEN}/sendMessage?chat_id=963157022&text={latitude, longitude, message.get("edited_message").get("from").get("username")}')


if __name__ == '__main__':
    run()