from instagram_handler import get_new_posts
from telegram_handler import send_posts_to_channel
import asyncio

async def main():
    while True:
        print("Getting new posts from Instagram...")
        new_posts = get_new_posts()
        
        print("Sending new posts to Telegram channel...")
        await send_posts_to_channel(new_posts)
        
        print("Look again for new posts in 1 minute\n")
        await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())