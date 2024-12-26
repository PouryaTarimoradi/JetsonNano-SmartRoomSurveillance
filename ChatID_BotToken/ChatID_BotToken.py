import requests
import time


def get_bot_and_chat_ids(token):
    # Extract bot ID from token
    bot_id = token.split(':')[0]

    # Base URL for Telegram Bot API
    base_url = f"https://api.telegram.org/bot{token}/"

    # Function to get updates
    def get_updates(offset=0):
        params = {'offset': offset, 'timeout': 30}
        response = requests.get(base_url + 'getUpdates', params=params)
        return response.json()['result']

    print(f"Bot ID: {bot_id}")
    print("Waiting for messages. Send a message to your bot...")

    # Keep track of the last update_id
    last_update_id = 0

    while True:
        updates = get_updates(last_update_id + 1)
        for update in updates:
            last_update_id = update['update_id']
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                user_id = update['message']['from']['id']
                print(f"New message - Chat ID: {chat_id}, User ID: {user_id}")

                # Send a response with the Chat ID
                response_text = f"Your Chat ID is: {chat_id}"
                params = {'chat_id': chat_id, 'text': response_text}
                requests.get(base_url + 'sendMessage', params=params)

        time.sleep(1)


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = "       "

try:
    get_bot_and_chat_ids(bot_token)
except KeyboardInterrupt:
    print("\nBot stopped.")
