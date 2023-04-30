import telegram
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

def send_posts_to_channel(posts):
    # Iniciar bot de Telegram
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    # Enviar cada publicación al canal de Telegram
    for post in posts:
        caption = f"{post.caption}\n\n{post.shortcode}"
        media = post.url
        bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=media, caption=caption)
