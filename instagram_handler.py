import logging
import os

# Create logger
logger = logging.getLogger("__main__.instagram_handler")

def log_in_to_instagram(cl, username):
    logger.info("Log in to Instagram")
    password = os.getenv("INSTAGRAM_PASSWORD")
    cl.login(username, password)

    return cl

def get_latest_posts(cl, user_id):    
    logger.info("Getting last 10 posts from Instagram...")
    latest_posts = cl.user_medias(user_id, 10)
    
    logger.info("Sorting Instagram posts by date")
    latest_posts_sorted = sorted(latest_posts, key=lambda post: post.taken_at)

    return latest_posts_sorted