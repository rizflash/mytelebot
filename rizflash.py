import telebot
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    start_text = """
Halo! Saya adalah bot moderator untuk request.

Untuk melihat cara membuat request, silakan gunakan perintah /help.
"""
    bot.reply_to(message, start_text)

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
Untuk request silakan pakai format:
`!req <requestmu>`

*Contoh:*
`!req Ben 10 Alien Force S01E11`
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['id'])
def send_id(message):
    if message.chat.type == 'private':
        bot.reply_to(message, f"Chat ID Anda adalah: `{message.chat.id}`")
    else:
        bot.reply_to(message, "Perintah ini hanya bisa digunakan di chat pribadi dengan bot.")

@bot.message_handler(func=lambda message: message.text is not None and message.text.lower().startswith('!req'))
def handle_request(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "Tolong sertakan request kau setelah perintah.\nContoh: `!req dexter resurrection s01e01`", parse_mode='Markdown')
        return
        
    request_text = message.text.split(maxsplit=1)[1]

    user = message.from_user
    username = f"@{user.username}" if user.username else user.first_name
    chat_title = message.chat.title if message.chat.title else "Private Chat"
    
    admin_message = f"""
**New Request!**

**From**: {username} (ID: `{user.id}`)
**Group**: {chat_title}

**Request**:
`{request_text}`
"""

    try:
        bot.send_message(ADMIN_ID, admin_message, parse_mode='Markdown')
        bot.reply_to(message, f"Requestmu untuk '{request_text}' telah diteruskan ke admin!")
    except Exception as e:
        print(f"Error mengirim pesan ke admin: {e}")
        bot.reply_to(message, "Maaf, terjadi kesalahan saat mengirim request ke admin. Silakan coba lagi nanti.")

print("Bot sedang berjalan...")
bot.infinity_polling()
