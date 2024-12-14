# Idle Mode

## Overview
The Idle Mode module ensures that the surveillance system can be paused and resumed as needed. When idle mode is active, the system stops processing motion detection, notifications, and other tasks, conserving resources while remaining ready to resume operations. This feature is essential for optimizing resource usage and giving users full control over the system's activity.

## Features
- Pauses and resumes the surveillance system without terminating the program.
- Integrates seamlessly with Telegram bot commands for remote activation and deactivation.
- Provides console feedback on the system's current state (Active or Idle).
- Allows real-time switching between modes without disrupting the overall system.
- Prevents resource-intensive operations like image processing and notifications during idle mode.

## How It Works
The `idle_mode.py` script operates as a control mechanism that toggles the system's operational state. Here's how it works:

1. **State Management**:
   - Maintains a boolean flag (`is_idle`) to track whether the system is in idle mode.
   - When idle mode is active, key functionalities such as motion detection, notifications, and image processing are disabled.

2. **Command Handling**:
   - Listens for external commands (e.g., from a Telegram bot) to switch between active and idle modes.
   - Processes commands such as `Start` to resume operations and `Stop` to enter idle mode.

3. **Feedback**:
   - Outputs the current state (`Active` or `Idle`) to the console and sends state updates to the Telegram bot for remote monitoring.

4. **Integration**:
   - Can be integrated into the main surveillance system to dynamically control processing tasks.

## Setup Instructions
1. Ensure the Telegram bot integration is configured correctly (see `bot_config.py`).
2. Import the `idle_mode.py` module in the main system script to enable state control.
3. Update the command-handling logic in the Telegram bot script to include `Start` and `Stop` commands for idle mode management.

## Usage
### Activating Idle Mode
Call the `set_idle_mode()` function with `True` to activate idle mode:
```python
from idle_mode import set_idle_mode
set_idle_mode(True)
```
This pauses the surveillance system, stopping motion detection and notifications.

### Resuming Operations
Call the `set_idle_mode()` function with `False` to deactivate idle mode:
```python
set_idle_mode(False)
```
This resumes all suspended operations.

### Checking Idle State
You can check whether the system is currently in idle mode:
```python
from idle_mode import is_idle
if is_idle:
    print("The system is currently idle.")
else:
    print("The system is active.")
```

## Code Snippet Breakdown
### State Management
```python
# Global flag for idle mode
is_idle = False

def set_idle_mode(state):
    global is_idle
    is_idle = state
    if is_idle:
        print("System is now in Idle Mode.")
    else:
        print("System is now Active.")
```
This function sets the `is_idle` flag and provides feedback on the current system state.

### Command Handling Example
```python
def handle_command(command):
    if command.lower() == "start":
        set_idle_mode(False)
    elif command.lower() == "stop":
        set_idle_mode(True)
    else:
        print("Unknown command.")
```
This function interprets commands (e.g., from a Telegram bot) to toggle the system's state.

### Integration with Main Script
```python
from idle_mode import is_idle, set_idle_mode

while True:
    if not is_idle:
        # Perform motion detection and other tasks
        print("System is Active: Processing...")
    else:
        print("System is Idle: No operations performed.")
    time.sleep(1)
```
This ensures that motion detection only runs when the system is active.

### Telegram Command Example
Integrate idle mode with Telegram bot commands:
```python
@bot.message_handler(commands=['start', 'stop'])
def handle_telegram_commands(message):
    if message.text.lower() == "/start":
        set_idle_mode(False)
        bot.send_message(chat_id, "System is now Active.")
    elif message.text.lower() == "/stop":
        set_idle_mode(True)
        bot.send_message(chat_id, "System is now in Idle Mode.")
```
This allows users to toggle idle mode directly from the Telegram bot.

## Example Output
- **Console Logs**:
  ```
  System is now in Idle Mode.
  System is now Active.
  ```
- **Telegram Bot Messages**:
  ```
  User: /stop
  Bot: System is now in Idle Mode.
  User: /start
  Bot: System is now Active.
  ```

## Integration Example
In the main script, integrate idle mode with motion detection:
```python
from idle_mode import is_idle

while True:
    if not is_idle:
        # Perform motion detection and other tasks
        print("System is Active: Processing...")
    else:
        print("System is Idle: No operations performed.")
    time.sleep(1)
```
This ensures that motion detection only runs when the system is active.

## Dependencies
- Python 3.6 or higher

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

