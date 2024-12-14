import telegram
import time
import threading
import json
import os
from bot_config import bot, chat_id
from send_telegram import store_message_id, MESSAGE_IDS_FILE, send_message_via_telegram
from system_stats import get_temperature, get_cpu_usage, get_ram_usage

# Create threading.Event objects for system activity and exit events
system_active_event = threading.Event()  # Initially, the system is idle (not set)
exit_event = threading.Event()  # This will signal when the system should exit
image_detection_paused = threading.Event()  # Event to manage image detection pausing

# Set the image detection paused to True initially to make sure it's paused until "Start" is pressed
image_detection_paused.set()  # Start in a paused state

def delete_all_messages():
    """Deletes all messages stored in the message_ids.json file."""
    if os.path.exists(MESSAGE_IDS_FILE):
        with open(MESSAGE_IDS_FILE, 'r') as f:
            message_ids = json.load(f)

        for message_id in message_ids:
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception as e:
                print(f"Failed to delete message {message_id}: {e}")

        # Clear the message IDs after deletion
        with open(MESSAGE_IDS_FILE, 'w') as f:
            json.dump([], f)

        print("All messages have been deleted.")
    else:
        print("No message IDs file found. Nothing to delete.")

def send_command_buttons():
    """Sends the command buttons to Telegram."""
    initialization_message = (
        "System is ready. Please press the appropriate button to control the system."
    )
    send_message_via_telegram(initialization_message, with_buttons=True)

def handle_callback_query(update):
    query = update.callback_query
    message = query.data.strip().lower()

    # Handle button presses
    if message == 'start':
        image_detection_paused.clear()  # Resume image detection
        system_active_event.set()  # Activate the system
        sent_message = bot.send_message(chat_id=query.message.chat_id, text="System activated. Motion detection is ON.")
        store_message_id(sent_message.message_id)
    elif message == 'stop':
        system_active_event.clear()  # Deactivate the system
        image_detection_paused.set()  # Pause image detection
        sent_message = bot.send_message(chat_id=query.message.chat_id, text="System deactivated. Motion detection is OFF.")
        store_message_id(sent_message.message_id)
    elif message == 'status':
        status = "active" if system_active_event.is_set() else "idle"
        sent_message = bot.send_message(chat_id=query.message.chat_id, text=f"The system is currently {status}.")
        store_message_id(sent_message.message_id)
    elif message == 'clean':
        delete_all_messages()
        sent_message = bot.send_message(chat_id=query.message.chat_id, text="All messages and images have been deleted.")
        store_message_id(sent_message.message_id)
        image_detection_paused.set()  # Pause image detection
        send_command_buttons()  # Resend buttons after cleaning
    elif message == 'system':
        temp = get_temperature()
        cpu = get_cpu_usage()
        ram = get_ram_usage()

        if temp is not None and cpu is not None and ram is not None:
            status_message = (
                f"CPU Temperature: {temp:.2f}°C\n"
                f"CPU Usage: {cpu:.1f}%\n"
                f"RAM Usage: {ram:.1f}%\n"
            )
        else:
            status_message = "Error reading system stats."
        sent_message = bot.send_message(chat_id=query.message.chat_id, text=status_message)
        store_message_id(sent_message.message_id)
    elif message == 'exit':
        exit_event.set()  # Signal the main program to exit
        sent_message = bot.send_message(chat_id=query.message.chat_id, text="Exiting the system...")
        store_message_id(sent_message.message_id)
        print("Exit command received. Exiting the system.")
    else:
        sent_message = bot.send_message(
            chat_id=query.message.chat_id,
            text="Unknown command. Available commands are: start, stop, status, clean, system."
        )
        store_message_id(sent_message.message_id)

    query.answer()  # Acknowledge the callback query

def handle_text_message(update):
    """Handle text commands sent via Telegram."""
    message = update.message.text.strip().lower()

    if message == 'c' or message == 'commands':
        # Resend command buttons
        send_command_buttons()
        image_detection_paused.set()  # Pause image detection
    else:
        sent_message = bot.send_message(
            chat_id=update.message.chat_id,
            text="Unknown command. Available commands are: start, stop, status, clean, system."
        )
        store_message_id(sent_message.message_id)

def idle_mode_listener():
    """Manually polls for new messages and handles them."""
    try:
        # Skip old updates by setting the offset to the latest update
        updates = bot.get_updates()
        update_id = updates[-1].update_id + 1 if updates else None
    except Exception as e:
        print(f"Error while fetching updates: {e}")
        update_id = None

    while not exit_event.is_set():  # Stop polling when exit is requested
        try:
            updates = bot.get_updates(offset=update_id, timeout=10)
            for update in updates:
                update_id = update.update_id + 1  # Move to the next update
                if update.message and update.message.text:
                    handle_text_message(update)
                elif update.callback_query:
                    handle_callback_query(update)
        except telegram.error.TimedOut:
            continue  # Retry on timeout
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  # Short delay before retrying

def initialize_idle_mode():
    """Initialize the idle mode listener in a separate thread."""
    thread = threading.Thread(target=idle_mode_listener)
    thread.daemon = True  # This makes sure the thread will exit when the main program does
    thread.start()
