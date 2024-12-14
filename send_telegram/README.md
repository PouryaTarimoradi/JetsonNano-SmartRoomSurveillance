# Telegram Integration

## Overview
The Telegram Integration module facilitates communication between the surveillance system and the Telegram bot. This module allows the system to send notifications, images, and interactive buttons to users, ensuring seamless control and updates in real time. Additionally, it manages the deletion of messages for a clean and user-friendly interface. The module also leverages multithreading and a thread-safe queue to handle communication tasks efficiently, ensuring responsiveness even during high system load.

## Features
- **Message Sending**: Sends real-time text notifications, images, and detection data to the Telegram bot.
- **Interactive Buttons**: Provides inline keyboard buttons for controlling the system (e.g., start, stop, clean, system, and exit).
- **Message Management**: Tracks message IDs to enable cleanup of old messages when required.
- **Thread-Safe Queue**: Uses a queue to process and manage messages asynchronously.
- **Threading Support**: Handles Telegram bot communication in a separate worker thread to avoid blocking the main program.
- **Command Shortcuts**: Allows users to send `C` or `c` to the bot to resend the command options (buttons).
- **Integration**: Works seamlessly with other modules, such as `idle_mode` and `system_stats`.

## How It Works
1. **Threading and Queue Management**:
   - A dedicated worker thread processes messages and images from a thread-safe queue (`queue.Queue`).
   - Ensures non-blocking communication and efficient resource usage.

2. **Sending Messages and Images**:
   - Uses the Telegram Bot API to send text, images, and detection data to the bot.
   - Supports attaching interactive buttons for user commands.

3. **Message ID Management**:
   - Stores sent message IDs in a JSON file (`message_ids.json`) for efficient deletion.
   - Cleans up messages from the chat when requested via the `/clean` command.

4. **Interactive Control**:
   - Displays inline keyboard buttons to users for controlling the system.
   - Handles button presses using callback queries processed in real time.

5. **Command Shortcuts**:
   - Users can send `C` or `c` to the bot to resend the command buttons, ensuring easy access to controls.

## Setup Instructions
1. Ensure the Telegram bot is configured in `bot_config.py`.
2. Import this module wherever Telegram messaging is required.
3. Start the worker thread to process Telegram messages and images asynchronously.

## Usage
### Sending a Message
To send a simple text message:
```python
from send_telegram import send_message_via_telegram
send_message_via_telegram("Hello from the surveillance system!")
```

### Sending a Message with Buttons
To send a message with inline keyboard buttons:
```python
send_message_via_telegram(
    "Choose an action:",
    with_buttons=True
)
```

### Sending an Image
To queue an image for sending:
```python
from send_telegram import send_image_via_telegram
send_image_via_telegram("path/to/image.jpg", detection_data="Person detected")
```

### Cleaning Up Messages
To delete all messages stored in `message_ids.json`:
```python
from send_telegram import delete_all_messages
delete_all_messages()
```

### Stopping the Worker Thread
To gracefully stop the worker thread:
```python
from send_telegram import stop_telegram_worker
stop_telegram_worker()
```

## Code Snippet Breakdown
### Thread-Safe Queue and Worker Thread
```python
import threading
import queue
from bot_config import bot, chat_id

# Create a thread-safe queue for sending messages
send_queue = queue.Queue()

def telegram_worker():
    """Worker thread that sends messages and images from the queue."""
    while True:
        item = send_queue.get()
        if item is None:
            break  # Exit signal received
        try:
            if item['type'] == 'message':
                if 'reply_markup' in item:
                    sent_message = bot.send_message(chat_id=chat_id, text=item['content'], reply_markup=item['reply_markup'])
                else:
                    sent_message = bot.send_message(chat_id=chat_id, text=item['content'])
                store_message_id(sent_message.message_id)
            elif item['type'] == 'image':
                with open(item['path'], 'rb') as image_file:
                    sent_message = bot.send_photo(chat_id=chat_id, photo=image_file)
                    store_message_id(sent_message.message_id)
            elif item['type'] == 'detection_data':
                sent_message = bot.send_message(chat_id=chat_id, text=item['content'])
                store_message_id(sent_message.message_id)
        except Exception as e:
            print(f"Error sending {item['type']} to Telegram: {e}")
        finally:
            send_queue.task_done()

# Start the worker thread
worker_thread = threading.Thread(target=telegram_worker, daemon=True)
worker_thread.start()
```
This thread processes all message and image requests from the queue, ensuring that communication tasks run asynchronously.

### Sending Messages and Images
```python
def send_message_via_telegram(message, with_buttons=False):
    if with_buttons:
        keyboard = [
            [InlineKeyboardButton("Start", callback_data='start'),
             InlineKeyboardButton("Stop", callback_data='stop')],
            [InlineKeyboardButton("Status", callback_data='status'),
             InlineKeyboardButton("Clean", callback_data='clean')],
            [InlineKeyboardButton("System", callback_data='system'),
             InlineKeyboardButton("Exit", callback_data='exit')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        send_queue.put({'type': 'message', 'content': message, 'reply_markup': reply_markup})
    else:
        send_queue.put({'type': 'message', 'content': message})


def send_image_via_telegram(image_path, detection_data=None):
    if os.path.exists(image_path):
        send_queue.put({'type': 'image', 'path': image_path})
        if detection_data:
            send_queue.put({'type': 'detection_data', 'content': detection_data})
    else:
        print(f"Image not found: {image_path}")
```
These functions add messages and images to the queue for asynchronous processing.

### Deleting Messages
```python
import os
import json

MESSAGE_IDS_FILE = "message_ids.json"

def delete_all_messages():
    if os.path.exists(MESSAGE_IDS_FILE):
        with open(MESSAGE_IDS_FILE, "r") as f:
            message_ids = json.load(f)

        for message_id in message_ids:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                print(f"Failed to delete message {message_id}: {e}")

        with open(MESSAGE_IDS_FILE, "w") as f:
            json.dump([], f)

        print("All messages have been deleted.")
    else:
        print("No message IDs file found. Nothing to delete.")
```
This function removes all tracked messages from the Telegram chat.

## Example Output
- **Telegram Message**:
  ```
  Hello from the surveillance system!
  ```
- **With Buttons**:
  ```
  Choose an action:
  [ Start | Stop ]
  [ Clean | Status ]
  [ System | Exit ]
  ```
- **Image Sent**:
  ```
  Image sent: path/to/image.jpg
  Detection Data: Person detected
  ```
- **Command Shortcut (`C` or `c`)**:
  ```
  Control the system:
  [ Start | Stop ]
  [ Clean | Status ]
  [ System | Exit ]
  ```

## Dependencies
- Python 3.6 or higher
- `python-telegram-bot` library

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

