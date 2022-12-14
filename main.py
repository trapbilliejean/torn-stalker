import requests
import time
from urllib import request, parse
from configparser import ConfigParser
from keep_alive import keep_alive

# Reading from Configfile
config = ConfigParser()
config.read('config.ini')

api_key = config.get('PERSONAL SETTINGS', 'api_key')
chanify_token = config.get('PERSONAL SETTINGS', 'chanify_token')
victims = config.get('PROGRAMM SETTINGS', 'victims').split(',')

print(api_key, chanify_token, victims)

def send_not(notification_message):
    data = parse.urlencode({ 'text': notification_message }).encode()
    req = request.Request(f'https://api.chanify.net/v1/sender/{chanify_token}', data=data)
    request.urlopen(req)

victims_list = []

for x in victims:
    api_call = requests.get(f'https://api.torn.com/user/{x}?selections=&key={api_key}').json()
    init_id = x
    init_name = api_call['name']
    init_current_state = api_call['status']['state']
    init_details = api_call['status']['details']
    init_previous_status = ''
    victims_list.append([str(init_previous_status),str(init_current_state), str(init_id), str(init_name), str(init_details)])
    time.sleep(0.1)

keep_alive()

while True:
    for x in victims_list:
        api_call = requests.get(f'https://api.torn.com/user/{x[2]}?selections=&key={api_key}').json()
        time.sleep(1)
        if x[0] == '' or not x[0].__contains__(api_call['status']['state']):
            x[0] = api_call['status']['state']
            x[1] = ''
            print(x[0])
            update = True
        else:
            x[1] = ""
            continue

    message = ''

    if update:
        for each in victims_list:
            print(each)
            message += ' '.join(' '.join(each).split())
            message += "\n"
        send_not(message)
        update = False
        print(message)
    time.sleep(29.9)
