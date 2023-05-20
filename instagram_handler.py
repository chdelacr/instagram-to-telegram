import logging
import os
import time
from sftp_handler import sftp_instagram_dump

# Create logger
logger = logging.getLogger("__main__.instagram_handler")

def log_in_to_instagram(cl, username):
    logger.info("Logging in to Instagram")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    try:
        # Load latest dump settings
        sftp_instagram_dump('l')
        
        logger.info("Attempting login with dump settings")
        cl.load_settings("local_dump.json")
        cl.login(username, password)
    except:
        logger.info("Unable to log in, retrying again by relogging in after 15 seconds")        
        time.sleep(15)
        
        # Create dump settings
        cl.login(username, password)
        cl.dump_settings("local_dump.json")
            
        sftp_instagram_dump('c')

    return cl

def get_latest_posts(cl, user_id):    
    logger.info("Getting last 10 posts from Instagram...")
    latest_posts = cl.user_medias(user_id, 10)
    
    logger.info("Sorting Instagram posts by date")
    latest_posts_sorted = sorted(latest_posts, key=lambda post: post.taken_at)

    return latest_posts_sorted