# Bot Configuration

## Overview
This module handles the configuration for the Telegram bot. It stores the bot's token, chat ID, and other settings required for interaction between the Jetson Nano and the Telegram API.

## Features
- Stores the Telegram bot token and chat ID.
- Provides configuration options for bot command handling.

## Setup Instructions
1. Obtain the bot token from [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
2. Save the token and chat ID in `ChatID_BotToken.py`.

## Usage
This module is imported by other scripts (e.g., `send_telegram.py`) to access the bot's configuration.

## Example Configuration
```python
# ChatID_BotToken.py
BOT_TOKEN = "your_bot_token_here"
CHAT_ID = "your_chat_id_here"
```

## Dependencies
- Python 3.6 or higher
- python-telegram-bot (version 13.12)

## License
This module is part of the AI-Powered Surveillance System. See the main project `LICENSE` file for details.

