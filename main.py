import asyncio
import logging
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
    # Load environment variables
    load_dotenv()

    # Log in to Instagram
    cl, username = log_in_to_instagram()

    while True:
        # Get latest posts from Instagram
        posts = get_latest_posts(cl, username)
        
        # Send new posts to Telegram channel
        await send_posts_to_channel(posts)
        
        logger.info(f"Look again for new posts in {run_interval // 60} minutes\n")
        await asyncio.sleep(run_interval)

if __name__ == '__main__':
    asyncio.run(main())