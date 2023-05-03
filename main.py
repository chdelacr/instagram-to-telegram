import instagrapi
import os
import asyncio
from dotenv import load_dotenv
from instagram_handler import get_latest_posts
from telegram_handler import send_posts_to_channel

async def main():
    # Load environment variables
    load_dotenv()

    print("Login into Instagram...")
    cl = instagrapi.Client()
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    cl.login(username, password)

    while True:
        print("Getting latest posts from Instagram...")
        posts = get_latest_posts(cl, username)
        
        print("Sending new posts to Telegram channel...")
        await send_posts_to_channel(posts)
        
        print("Look again for new posts in 15 minutes\n")
        await asyncio.sleep(900)

if __name__ == '__main__':
    asyncio.run(main())