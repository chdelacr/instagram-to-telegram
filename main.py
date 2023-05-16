import asyncio
import instagrapi
import logging
import os
from dotenv import load_dotenv
from instagram_handler import log_in_to_instagram, get_latest_posts
from telegram_handler import send_posts_to_channel

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Define time interval (in seconds)
run_interval = 1800

async def main():
    cl = instagrapi.Client()
    
    # Load environment variables
    load_dotenv()
    username = os.getenv("INSTAGRAM_USERNAME")
    
    if os.getenv("PRIVATE_ACCESS") == "Y":
        # Log in to Instagram
        cl = log_in_to_instagram(cl, username)
        
    # Get id from Instagram username
    try:
        user_id = cl.user_id_from_username(username)
    except:
        # Retry by log in into Instagram
        logger.info("Unable to get user ID from public data, retrying again by logging in")
        cl = log_in_to_instagram(cl, username)
        user_id = cl.user_id_from_username(username)

    while True:
        # Get latest posts from Instagram
        posts = get_latest_posts(cl, user_id)
        
        # Send new posts to Telegram channel
        await send_posts_to_channel(posts)
        
        logger.info(f"Look again for new posts in {run_interval // 60} minutes\n")
        await asyncio.sleep(run_interval)

if __name__ == '__main__':
    asyncio.run(main())