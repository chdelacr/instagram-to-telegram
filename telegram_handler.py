import telegram
import os
import pysftp
from datetime import datetime

async def send_posts_to_channel(posts):
    print("Starting Telegram bot...")
    bot = telegram.Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
    
    print("Reading identifier of previous Instagram posts sent to Telegram channel...")
    print("Connecting to SFTP...")
    sent_posts = set()
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    sftp_server = os.getenv("SFTP_SERVER")
    sftp_username = os.getenv("SFTP_USERNAME")
    sftp_password = os.getenv("SFTP_PASSWORD")
    sftp_path = os.getenv("SFTP_PATH")

    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'sent_posts_{current_date}.txt'
    
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        with sftp.cd(sftp_path):
            if sftp.exists(filename):
                print("Reading checkpoint file...")
                with sftp.open(filename, 'r') as f:
                    sent_posts = set([line.strip() for line in f.readlines()])

    print("Sending only new posts (only picture, not part of albums) to Telegram channel...")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    for post in posts:
        if f'{post.pk}_{post.code}_{post.taken_at}' not in sent_posts and post.media_type == 1:
            print("Sending picture and caption to Telegram channel...")
            thumbnail_url = post.thumbnail_url
            caption = post.caption_text
            await bot.send_photo(chat_id=channel_id, photo=thumbnail_url, caption=caption)

            sent_posts.add(f'{post.pk}_{post.code}_{post.taken_at}')

    print("Saving identifier of new posts (if any) sent to Telegram channel...")
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        with sftp.cd(sftp_path):
            with sftp.open(filename, 'w') as f:
                f.write('\n'.join(sent_posts))

            print("Deleting files in SFTP that are older than 7 days...")
            for file in sftp.listdir():
                if file.startswith('sent_posts_'):
                    file_path = f'{sftp_path}/{file}'
                    mtime = sftp.stat(file_path).st_mtime
                    if (datetime.now() - datetime.fromtimestamp(mtime)).days > 7:
                        sftp.remove(file_path)