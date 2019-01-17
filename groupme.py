import requests
from access_token import ACCESS_TOKEN
import time

GROUPS_URL = "https://api.groupme.com/v3/groups"
MESSAGES_URL = "https://api.groupme.com/v3/groups/{}/messages"
PARTY_GROUP_CHAT_ID = '43504680'
SLEEP_DURATION = 5
MOVE_REQUEST = '/moves'

def listen_for_moves_request():
    message_params = get_messages_url_params()
    while True:
        response = request_messages(message_params)
        if is_good_response(response):

            messages = get_messages(response.json())
            messages = remove_empty_messages(messages)

            moves_is_requested = any(MOVE_REQUEST in message['text'] for message in messages)

            if moves_is_requested:
                moves = get_moves()
                post_moves(moves)
        
        last_message_id = messages[-1]['id']
        message_params['after_id'] = last_message_id

        time.sleep(SLEEP_DURATION)

def remove_empty_messages(messages):
    return [message for message in messages if message['text']]

def request_messages(message_params):
    messages_url = MESSAGES_URL.format(PARTY_GROUP_CHAT_ID)
    response = requests.get(messages_url, params=message_params)
    return response

def is_good_response(response):
    return response.status_code == 200

def get_messages_url_params(after_id=None):
    params = {
        'token': ACCESS_TOKEN,
        'limit': '20',
    }
    if after_id:
        params['after_id'] = after_id
    return params

def get_group_ids():
    response = requests.get(GROUPS_URL, params=get_groups_url_params())
    if is_good_response(response):
        json_data = response.json()
        return [group['id'] for group in json_data['response']]
    return None

def get_groups_url_params():
    return {
        'token': ACCESS_TOKEN,
        'per_page': 100
    }
    
def get_messages(json_data):
    return json_data['response']['messages']

def get_moves():
    return []

def post_moves(moves):
    pass