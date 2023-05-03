import telegram
import os
from sftp_handler import sftp_utils
from datetime import datetime

async def send_posts_to_channel(posts):
    print("Starting Telegram bot...")
    bot = telegram.Bot(os.getenv("TELEGRAM_BOT_TOKEN"))

    # Get sent posts from checkpoint file
    sent_posts = sftp_utils('r')
    
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    current_date = datetime.now()
    for post in posts:
        # Send only today's posts
        taken_at_converted = post.taken_at.astimezone(current_date.tzinfo)
        if taken_at_converted.date() == current_date.date() and f'{post.pk}_{post.code}_{post.taken_at}' not in sent_posts:
            if post.media_type == 1:
                print("Sending new picture post to Telegram channel...")
                photo = post.thumbnail_url
                caption = post.caption_text
                await bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)
            if post.media_type == 2:
                print("Sending new video post to Telegram channel...")
                video = post.video_url
                caption = post.caption_text
                await bot.send_video(chat_id=channel_id, video=video, caption=caption)
            # Disabling album handling since Telegram isn't showing captions properly
            """elif post.media_type == 8:
                print("Sending new album post to Telegram channel...")
                media_group = []
                caption = post.caption_text
                for p in post.resources:
                    if p.media_type == 1:
                        media_group.append(telegram.InputMediaPhoto(p.thumbnail_url, caption=caption))
                    elif p.media_type == 2:
                        media_group.append(telegram.InputMediaVideo(p.video_url, caption=caption))
                        
                await bot.send_media_group(chat_id=channel_id, media=media_group)"""

            sent_posts.add(f'{post.pk}_{post.code}_{post.taken_at}')

    sftp_utils('w', sent_posts)
    sftp_utils('d')