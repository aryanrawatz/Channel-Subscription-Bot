import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
CHANNEL_ID = os.getenv('CHANNEL_ID')  # Jaise: "@your_channel_username" ya "-100xxxxxxx"

bot = telebot.TeleBot(BOT_TOKEN)

# 1. Media Broadcaster Handler (Photo/Video to Channel with Payment Buttons)
@bot.message_handler(content_types=['photo', 'video'])
def handle_media_broadcast(message):
    # Only Admin can broadcast
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ Only Admin can broadcast media.")
        return

    bot_info = bot.get_me()
    bot_username = bot_info.username

    # Subscription Payment Buttons
    markup = InlineKeyboardMarkup()
    btn_pay = InlineKeyboardButton("💳 Buy Subscription / Access", url=f"https://t.me/{bot_username}?start=subscribe")
    markup.add(btn_pay)

    caption = message.caption if message.caption else "🔥 Exclusive Content - Click below to join!"

    try:
        if message.content_type == 'photo':
            # Send photo to channel
            photo_id = message.photo[-1].file_id
            bot.send_photo(CHANNEL_ID, photo_id, caption=caption, reply_markup=markup)
        
        elif message.content_type == 'video':
            # Send video to channel
            video_id = message.video.file_id
            bot.send_video(CHANNEL_ID, video_id, caption=caption, reply_markup=markup)

        bot.reply_to(message, "✅ Successfully posted to Channel with payment buttons!")
    except Exception as e:
        bot.reply_to(message, f"❌ Error posting to channel: {str(e)}")

# 2. Standard Start Command
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot_info = bot.get_me()
    bot_username = bot_info.username

    markup = InlineKeyboardMarkup()
    btn_30 = InlineKeyboardButton("💳 30 Days - ₹199", callback_data="pay_199")
    btn_contact = InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{bot_username}")
    markup.add(btn_30)
    markup.add(btn_contact)

    bot.send_message(
        message.chat.id,
        "Welcome! Choose a subscription plan to get full channel access:",
        reply_markup=markup
    )

if __name__ == '__main__':
    bot.infinity_polling()
