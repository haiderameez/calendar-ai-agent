# Calendar AI Agent
This is an AI agent that uses Telegram, Gemini and Google Calendar to add calendar events via Telegram messages.

## Usage Guide

### 1. Download the Repository

### 2. Install all the dependencies using the following line of code:
```python
pip install -r requirements.txt
```

### 3. Environment Variables
- Set up the environment variables of the Telegram bot and Gemini.
- Use Telegram's BotFather to create a bot and get the credentials for the bot.
- Similarly, get Gemini API key using https://ai.google.dev/gemini-api/docs/api-key
- Store these two in a `.env` file
```.env
GEMINI_API_KEY = your_gemini_api_key
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
```


### 4. Setting up Google Calendar   
- Go to https://developers.google.com/workspace/guides/create-credentials to get the `credentials.json` file of the Google Calendar.
- The scope in `config.py` is set to https://www.googleapis.com/auth/calendar.
  
### 5. Example Usage
- Run `main.py`
- Go to the Telegram Bot and send a message like "Set a meeting with John on 4th March 2025 from 5:00pm to 6:00pm"..
- This will create an event in the Google Calendar.
