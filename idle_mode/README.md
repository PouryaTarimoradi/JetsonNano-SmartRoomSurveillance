# Idle Mode

## Overview
The Idle Mode module manages the operational state of the AI-powered surveillance system. It allows users to remotely pause or resume system activities, such as motion detection, image processing, and notifications, while ensuring smooth transitions between states. The module leverages multithreading for concurrent task management, ensuring that system responsiveness and key operations are maintained.

## Features
- **Remote Control**: Integrates with Telegram bot commands to toggle between active and idle states.
- **Multithreading**: Uses threads to handle Telegram command processing, system state management, and image detection independently.
- **Event Management**: Implements threading events to control and monitor system activities such as image detection and exit signals.
- **System Feedback**: Provides real-time updates on the system state (active or idle).

## How It Works
1. **Threading and Events**:
   - Uses `threading.Event` objects to manage system activities, such as pausing image detection and signaling program termination.
   - Separate threads ensure that Telegram updates and system tasks run concurrently without blocking each other.

2. **Command Handling**:
   - Listens for commands (`start`, `stop`, `status`, `clean`, etc.) via the Telegram bot.
   - Executes corresponding actions, such as resuming or pausing motion detection, deleting messages, or retrieving system stats.

3. **System Initialization**:
   - Starts a listener thread to continuously process Telegram commands.
   - Keeps the system idle (paused) by default until activated via the `start` command.

## Setup Instructions
1. Configure the Telegram bot using `bot_config.py`.
2. Ensure that the necessary modules (`send_telegram`, `system_stats`, etc.) are set up correctly.
3. Import and initialize the `idle_mode.py` module in the main script to enable remote state control.

## Usage
### Activating Idle Mode
The system starts in idle mode by default. Use the `/stop` command to explicitly set the system to idle mode:
```python
from idle_mode import image_detection_paused
image_detection_paused.set()  # Pause image detection
```

### Resuming Operations
Use the `/start` command to resume operations:
```python
from idle_mode import image_detection_paused
image_detection_paused.clear()  # Resume image detection
```

### Listening for Telegram Commands
Initialize the idle mode listener to process Telegram commands:
```python
from idle_mode import initialize_idle_mode
initialize_idle_mode()
```

## Code Snippet Breakdown
### Thread and Event Management
```python
import threading

# Events for system control
system_active_event = threading.Event()  # Indicates if the system is active
exit_event = threading.Event()  # Signals when to exit the program
image_detection_paused = threading.Event()  # Manages image detection state

# Start in a paused state
image_detection_paused.set()  # Ensures motion detection is paused until activated
```
These threading events allow precise control over system states, ensuring tasks like motion detection only run when appropriate.

### Telegram Command Handling
```python
def handle_callback_query(update):
    query = update.callback_query
    message = query.data.strip().lower()

    if message == 'start':
        image_detection_paused.clear()  # Resume image detection
        system_active_event.set()
        bot.send_message(chat_id=query.message.chat_id, text="System activated.")
    elif message == 'stop':
        image_detection_paused.set()  # Pause image detection
        system_active_event.clear()
        bot.send_message(chat_id=query.message.chat_id, text="System deactivated.")
    elif message == 'status':
        status = "active" if system_active_event.is_set() else "idle"
        bot.send_message(chat_id=query.message.chat_id, text=f"The system is currently {status}.")
    elif message == 'exit':
        exit_event.set()
        bot.send_message(chat_id=query.message.chat_id, text="Exiting the system...")
    query.answer()
```
This function processes commands received via Telegram and updates the system state accordingly.

### Idle Mode Listener
```python
def idle_mode_listener():
    """Polls Telegram for updates and handles commands."""
    while not exit_event.is_set():
        updates = bot.get_updates(timeout=10)
        for update in updates:
            if update.callback_query:
                handle_callback_query(update)
```
This thread continuously listens for and processes Telegram updates without blocking other system tasks.

### Initialization
```python
def initialize_idle_mode():
    thread = threading.Thread(target=idle_mode_listener)
    thread.daemon = True  # Ensures the thread stops when the main program exits
    thread.start()
    print("Idle Mode listener thread started.")
```
This initializes the listener thread, allowing the system to process Telegram commands independently.

## Example Output
- **Telegram Commands**:
  - `/start`: Activates the system and resumes motion detection.
  - `/stop`: Deactivates the system and pauses motion detection.
  - `/status`: Returns the current state (active or idle).
  - `/exit`: Stops all operations and exits the program.

- **Console Logs**:
  ```
  System is now active.
  System is now idle.
  Exiting the system...
  ```

## Dependencies
- Python 3.6 or higher
- `telegram` library for bot communication

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

