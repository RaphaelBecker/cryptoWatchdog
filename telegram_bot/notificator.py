import requests
import os

def post_message_to_chat_group(message_string):
    """
    Posts message to telegram group
    :param message_string:
    :return:
    """
    # TODO: add API key to env vars before release
    #api_key_url = os.environ.get('API_KEY_URL')
    api_key_url ='test_api_key_url'
    base_url = api_key_url + '{}'.format(message_string)
    print(message_string)
    requests.get(base_url)


def alert_rsi(coin_name, rsi, date_time):
    """
    :param coin_name:
    :param rsi: RSI-time_span value
    :param date_time: current date/time
    :return: void - shoots a message to the telegram group incase something interesting happens
    """
    rsi_upper_bound = 70
    rsi_lower_bound = 30
    if rsi > rsi_upper_bound:
        message = coin_name + ' is overbought. Time to sell! RSI = "{:.2f}"'.format(rsi)
        post_message_to_chat_group(message)
    elif rsi < rsi_lower_bound:
        message = coin_name + ' is oversold. Time to buy! RSI = "{:.2f}"'.format(rsi)
        post_message_to_chat_group(message)
    else:
        pass

def bot_ready(message):
    """
    send an initialization message to group
    :return:
    """
    post_message_to_chat_group(message)

