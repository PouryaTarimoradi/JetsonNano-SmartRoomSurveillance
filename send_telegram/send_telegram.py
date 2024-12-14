import os
import threading
import queue
import json
from bot_config import bot, chat_id
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Define the path for the JSON file to store message IDs
MESSAGE_IDS_FILE = "/home/pta/pyProject/Camera Control Security/message_ids.json"  # You can change this path as needed

# Create a thread-safe queue for sending messages
send_queue = queue.Queue()

def store_message_id(message_id):
    """
    Stores the message ID in a JSON file for future deletion.
    """
    if os.path.exists(MESSAGE_IDS_FILE):
        with open(MESSAGE_IDS_FILE, 'r') as f:
            message_ids = json.load(f)
    else:
        message_ids = []

    message_ids.append(message_id)

    with open(MESSAGE_IDS_FILE, 'w') as f:
        json.dump(message_ids, f)

def telegram_worker():
    """
    Worker thread that sends messages and images from the queue.
    """
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
                print("Message sent via Telegram.")
            elif item['type'] == 'image':
                with open(item['path'], 'rb') as image_file:
                    sent_message = bot.send_photo(chat_id=chat_id, photo=image_file)
                    store_message_id(sent_message.message_id)
                print("Image sent via Telegram.")
            elif item['type'] == 'detection_data':
                sent_message = bot.send_message(chat_id=chat_id, text=item['content'])
                store_message_id(sent_message.message_id)
                print("Detection data sent via Telegram.")
        except Exception as e:
            print(f"Error sending {item['type']} to Telegram: {e}")
        finally:
            send_queue.task_done()

# Start the worker thread
worker_thread = threading.Thread(target=telegram_worker, daemon=True)
worker_thread.start()

def send_image_via_telegram(image_path, detection_data=None):
    """
    Queues an image and optional detection data to be sent via Telegram.
    """
    if os.path.exists(image_path):
        # Queue the image for sending
        send_queue.put({'type': 'image', 'path': image_path})
        print(f"Queued image {image_path} for sending via Telegram.")

        # Queue the detection data if provided
        if detection_data:
            send_queue.put({'type': 'detection_data', 'content': detection_data})
            print("Queued detection data for sending via Telegram.")
    else:
        print(f"Image not found: {image_path}")

def send_message_via_telegram(message, with_buttons=False):
    """
    Queues a message to be sent via Telegram. If with_buttons is True, it sends an inline keyboard.
    """
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
    print("Queued message for sending via Telegram.")

def stop_telegram_worker():
    """
    Stops the worker thread gracefully.
    """
    send_queue.put(None)  # Send exit signal to the worker thread
    worker_thread.join()
    print("Telegram worker thread has been stopped.")
