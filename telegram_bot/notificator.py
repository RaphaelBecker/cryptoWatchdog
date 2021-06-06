import requests


def post_message_to_chat_group(message_string):
    """
    Posts message to telegram group
    :param message_string:
    :return:
    """
    # TODO: add API key to env vars before release
    # api_key_url = os.environ.get('API_KEY_URL_MESSAGE')
    api_key_url_message = 'https://api.telegram.org/bot1597486965:AAGIjRUzD9NTJfaeOgjvmSDNyMAL6NQ7O5c/sendMessage' \
                          '?chat_id' \
                          '=-1001424139495&text='
    base_url_message = api_key_url_message + '{}'.format(message_string)
    print(message_string)
    resp = requests.get(base_url_message)
    print('POST_MESSAGE_LOG: ' + resp.text)


def post_photo_to_chat_group(caption_string, ticker_symbol):
    """
    Posts photo to telegram group
    :param caption_string:
    :param ticker_symbol:
    :photo:
    :return:
    """
    file_path = './visualization/plots/' + ticker_symbol + '.png'
    print(file_path)
    mode = 'rb'  # read and byte mode
    file = {'photo': open(file_path, mode)}
    # TODO: add API key to env vars before release
    # api_key_url_photo = os.environ.get('API_KEY_URL_PHOTO')
    api_key_url_photo = 'https://api.telegram.org/bot1597486965:AAGIjRUzD9NTJfaeOgjvmSDNyMAL6NQ7O5c/sendPhoto?chat_id' \
                        '=-1001424139495&caption='
    base_url_photo = api_key_url_photo + caption_string
    resp = requests.post(base_url_photo, files=file)
    print('POST_PHOTO_LOG: ' + resp.text)


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
