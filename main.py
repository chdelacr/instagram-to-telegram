from instagram_handler import get_latest_posts
from telegram_handler import send_posts_to_channel
import instagrapi
import os
import asyncio

async def main():
    print("Login into Instagram...")
    cl = instagrapi.Client()
    username = os.environ['INSTAGRAM_USERNAME']
    password = os.environ['INSTAGRAM_PASSWORD']
    cl.login(username, password)

    while True:
        print("Getting latest posts from Instagram...")
        posts = get_latest_posts(cl, username)
        
        print("Sending new posts to Telegram channel...")
        await send_posts_to_channel(posts)
        
        print("Look again for new posts in 1 minute\n")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())