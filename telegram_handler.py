import telegram
import os
import pysftp

async def send_posts_to_channel(posts):
    print("Starting Telegram bot...")
    bot = telegram.Bot(os.environ['TELEGRAM_BOT_TOKEN'])

    print("Reading pks of previous Instagram posts sent to Telegram channel...")
    sent_posts = set()
    
    print("Connecting to SFTP...")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    sftp_server = os.environ['SFTP_SERVER']
    sftp_username = os.environ['SFTP_USERNAME']
    sftp_password = os.environ['SFTP_PASSWORD']
    sftp_path = os.environ['SFTP_PATH']
    
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        with sftp.cd(sftp_path):
            if sftp.exists('sent_posts.txt'):
                print("Reading checkpoint file...")
                with sftp.open('sent_posts.txt', 'r') as f:
                    sent_posts = set([line.strip() for line in f.readlines()])

    print("Sending only new posts to Telegram channel...")
    channel_id = os.environ['TELEGRAM_CHANNEL_ID']
    for post in posts:
        if post.pk not in sent_posts:
            print("Posting only Instagram picture (not part of albums)...")
            if post.media_type == 1:
                print("Getting Instagram picture URL...")
                thumbnail_url = post.thumbnail_url

                print("Sending picture and caption to Telegram channel...")
                caption = post.caption_text
                await bot.send_photo(chat_id=channel_id, photo=thumbnail_url, caption=caption)

                sent_posts.add(post.pk)

    print("Saving pks of new posts (if any) sent to Telegram channel...")
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        with sftp.cd(sftp_path):
            with sftp.open('sent_posts.txt', 'w') as f:
                f.write('\n'.join(sent_posts))