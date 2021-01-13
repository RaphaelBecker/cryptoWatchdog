import requests


def post_message_to_chat_group(message_string):
    base_url = 'https://api.telegram.org/bot1597486965:AAGIjRUzD9NTJfaeOgjvmSDNyMAL6NQ7O5c/sendMessage?chat_id=-416548268&text="{}"'.format(message_string)
    requests.get(base_url)


def alert_rsi(coin_name, rsi, date_time):
    rsi_upper_bound = 70
    rsi_lower_bound = 30
    if rsi > rsi_upper_bound:
        message = coin_name + " is overbought. Time to sell! RSI = " + str(rsi)
        post_message_to_chat_group(message)
    elif rsi > rsi_lower_bound:
        message = coin_name + " is oversold. Time to buy! RSI = " + str(rsi)
        post_message_to_chat_group(message)
    else:
        pass
