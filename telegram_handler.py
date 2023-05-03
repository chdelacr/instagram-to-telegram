import telegram
import os
from sftp_handler import sftp_utils

async def send_posts_to_channel(posts):
    print("Starting Telegram bot...")
    bot = telegram.Bot(os.getenv("TELEGRAM_BOT_TOKEN"))

    # Get sent posts from checkpoint file
    sent_posts = sftp_utils('r')
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    for post in posts:
        if f'{post.pk}_{post.code}_{post.taken_at}' not in sent_posts and post.media_type == 1:
            print("Sending only new posts (only picture, not part of albums) to Telegram channel...")
            thumbnail_url = post.thumbnail_url
            caption = post.caption_text
            await bot.send_photo(chat_id=channel_id, photo=thumbnail_url, caption=caption)

            sent_posts.add(f'{post.pk}_{post.code}_{post.taken_at}')

    sftp_utils('w', sent_posts)
    sftp_utils('d')