import requests

def post_message_to_chat_group(message_string):
    base_url = 'https://api.telegram.org/bot1597486965:AAGIjRUzD9NTJfaeOgjvmSDNyMAL6NQ7O5c/sendMessage?chat_id=-416548268&text="{}"'.format(message_string)
    requests.get(base_url)