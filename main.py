import os
import json
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = "primary"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

def get_calendar_service():
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return build("calendar", "v3", credentials=creds)

async def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text

    prompt = f"""
    Extract event details from this text:
    "{user_text}"
    
    Format the output as valid JSON:
    {{"summary": "Event title", "start": "YYYY-MM-DDTHH:MM:SS", "end": "YYYY-MM-DDTHH:MM:SS", "timeZone": "UTC"}}
    """

    try:
        response = model.generate_content(prompt)
        
        event_data = json.loads(response.text.strip("```json").strip("```"))  

        if all(k in event_data for k in ["summary", "start", "end"]):
            event_link = add_event_to_calendar(event_data)

            await update.message.reply_text(f"Event added: {event_data['summary']} on {event_data['start']}\n [View Event]({event_link})")
        else:
            await update.message.reply_text("I couldn't extract the event details properly. Please try again.")
    except json.JSONDecodeError:
        await update.message.reply_text("Gemini returned invalid data. Please try again.")
        print("Gemini JSON error:", response.text)
    except Exception as e:
        await update.message.reply_text("Error processing your request.")
        print("Error:", e)

def add_event_to_calendar(event_data):
    service = get_calendar_service()

    start_time = event_data["start"]
    end_time = event_data["end"]

    if "T" in start_time:
        event = {
            "summary": event_data["summary"],
            "start": {"dateTime": start_time, "timeZone": event_data.get("timeZone", "UTC")},
            "end": {"dateTime": end_time, "timeZone": event_data.get("timeZone", "UTC")},
        }
    else:  
        event = {
            "summary": event_data["summary"],
            "start": {"date": start_time},
            "end": {"date": end_time},
        }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return created_event.get("htmlLink") 


app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
