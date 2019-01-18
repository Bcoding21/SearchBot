import requests
from access_token import ACCESS_TOKEN
import time

GROUPS_URL = "https://api.groupme.com/v3/groups"
MESSAGES_URL_FORMAT = "https://api.groupme.com/v3/groups/{}/messages"
PARTY_GROUP_CHAT_ID = '43504680'
SLEEP_DURATION = 5
MOVE_REQUEST = '/moves'
KEYWORDS = []


def listen_for_moves_request():
    message_params = get_messages_url_params()
    while True:
        response = request_messages(message_params)

        messages = get_messages(response.json())
        messages = list(filter(contains_text, messages))

        moves_is_requested = any(contains_move_request(message)
                                 for message in messages)

        if moves_is_requested:
                moves = get_moves()
                post_moves(moves)

        if len(messages) > 0:
            last_message_id = messages[-1]['id']
            message_params['after_id'] = last_message_id

        time.sleep(SLEEP_DURATION)


def contains_move_request(message):
    return MOVE_REQUEST in message['text']


def contains_text(message):
    return message['text'] is not None


def request_messages(group_id, message_params):
    messages_url = MESSAGES_URL_FORMAT.format(group_id)
    response = requests.get(messages_url, params=message_params)
    return response.json() if is_good_response(response) else None


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
        group_chat_data = response.json()
        group_chats = group_chat_data['response']
        return [group['id'] for group in group_chats]
    return None


def get_groups_url_params():
    return {
        'token': ACCESS_TOKEN,
        'per_page': 100
    }


def get_messages(json_data):
    return json_data['response']['messages']


def get_moves():
    group_ids = get_group_ids()

    for group_id in group_ids:

        messages_url = MESSAGES_URL_FORMAT.format(group_id)

        messages_url_params = {
            'token': ACCESS_TOKEN,
            'limit': 100
        }

        response = requests.get(messages_url, params=messages_url_params)

        if is_good_response(response):

            messages = get_messages(response.json())

            messages = list(filter(contains_any_keywords, messages))


def contains_any_keywords(message):
    return any(keyword in message['text'] for keyword in KEYWORDS)


def post_moves(moves):
    pass
