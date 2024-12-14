# ChatID and BotToken Retrieval

## Overview
The ChatID and BotToken module simplifies the process of retrieving Chat IDs and User IDs for Telegram bot communication. This module waits for user interaction with the bot and extracts Chat IDs and User IDs from incoming messages. It is particularly useful during initial setup when configuring the Telegram bot to communicate with specific users.

## Features
- **Bot Token Parsing**: Extracts the Bot ID from the provided Bot Token.
- **Chat ID Retrieval**: Dynamically retrieves Chat IDs from incoming messages sent to the bot.
- **User ID Identification**: Identifies the User ID of the person sending the message.
- **Automated Response**: Sends a message back to the user with their Chat ID for confirmation.
- **Real-Time Updates**: Continuously polls Telegram for new messages.

## How It Works
1. **Bot Token Parsing**:
   - Extracts the Bot ID directly from the provided Bot Token.

2. **Real-Time Updates**:
   - Polls the Telegram Bot API using the `getUpdates` method to fetch new messages sent to the bot.

3. **Chat and User ID Extraction**:
   - Extracts Chat IDs and User IDs from the `getUpdates` response.
   - Sends a confirmation message back to the user containing their Chat ID.

4. **Continuous Polling**:
   - Uses a loop to keep listening for new messages.

## Setup Instructions
1. Obtain your Telegram Bot Token from the BotFather on Telegram.
2. Replace `YOUR_BOT_TOKEN` in the code with your actual Bot Token.
3. Run the script to start listening for messages sent to your bot.

## Usage
### Retrieving Chat IDs and User IDs
Run the script with your Bot Token to retrieve Chat IDs:
```bash
python3 chatid_bottoken.py
```

Send a message to your bot on Telegram. The script will output:
- The Chat ID
- The User ID
- A confirmation message sent back to the user with their Chat ID.

### Example
#### Console Output:
```
Bot ID: 123456789
Waiting for messages. Send a message to your bot...
New message - Chat ID: 987654321, User ID: 1122334455
```

#### Telegram Bot Response:
```
Your Chat ID is: 987654321
```

## Code Snippet Breakdown
### Bot Token Parsing
```python
def get_bot_and_chat_ids(token):
    # Extract bot ID from token
    bot_id = token.split(':')[0]
    print(f"Bot ID: {bot_id}")
```
This function parses the provided Bot Token to extract and print the Bot ID.

### Real-Time Updates
```python
def get_updates(offset=0):
    params = {'offset': offset, 'timeout': 30}
    response = requests.get(base_url + 'getUpdates', params=params)
    return response.json()['result']
```
This function polls the Telegram Bot API for new updates using the `getUpdates` method.

### Chat ID and User ID Retrieval
```python
while True:
    updates = get_updates(last_update_id + 1)
    for update in updates:
        last_update_id = update['update_id']
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            user_id = update['message']['from']['id']
            print(f"New message - Chat ID: {chat_id}, User ID: {user_id}")
```
This loop continuously listens for incoming messages and extracts Chat IDs and User IDs from the `getUpdates` response.

### Automated Response
```python
response_text = f"Your Chat ID is: {chat_id}"
params = {'chat_id': chat_id, 'text': response_text}
requests.get(base_url + 'sendMessage', params=params)
```
After extracting the Chat ID, this sends a confirmation message to the user with their Chat ID.

### Graceful Termination
```python
try:
    get_bot_and_chat_ids(bot_token)
except KeyboardInterrupt:
    print("\nBot stopped.")
```
Allows the script to terminate gracefully using a keyboard interrupt.

## Example Output
- **Console Logs**:
  ```
  Bot ID: 123456789
  Waiting for messages. Send a message to your bot...
  New message - Chat ID: 987654321, User ID: 1122334455
  ```
- **Telegram Bot Message**:
  ```
  Your Chat ID is: 987654321
  ```

## Dependencies
- Python 3.6 or higher
- `requests` library for HTTP communication

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

