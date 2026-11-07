from datetime import datetime
import requests
import pytz
import telebot

# بيانات البوت
TOKEN = "9080662768:AAG3E8DfD1-Ix_1nNQXbiriVZUu6-y6dCes"
bot = telebot.TeleBot(TOKEN)

# رابط تطبيق الويب الخاص بك
WEBHOOK_URL = "Https://script.google.com/macros/s/AKfycbzhg2S-8HyLyjiJwYsI3FxXygldK6PGmW6Jl6DbY9GOGoYEGcmuY5bs189LSKn3-LfD/exec"


def send_to_google_sheets(full_name, username, user_id, map_link):
  cairo_tz = pytz.timezone("Africa/Cairo")
  now = datetime.now(cairo_tz)
  arrival_time = now.strftime("%Y-%m-%d %I:%M:%S %p")

  payload = {
      "full_name": full_name,
      "username": username,
      "user_id": user_id,
      "arrival_time": arrival_time,
      "map_link": map_link,
  }

  try:
    requests.post(WEBHOOK_URL, json=payload)
  except Exception as e:
    print(f"Error sending to Google Sheets: {e}")


@bot.message_handler(content_types=["location"])
def handle_location(message):
  user = message.from_user
  full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
  username = f"@{user.username}" if user.username else "No Username"
  user_id = str(user.id)

  lat = message.location.latitude
  lon = message.location.longitude
  map_link = f"https://maps.google.com/?q={lat},{lon}"

  send_to_google_sheets(full_name, username, user_id, map_link)


print("Bot is running...")
bot.infinity_polling()