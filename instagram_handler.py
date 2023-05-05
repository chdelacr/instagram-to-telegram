import logging
import instagrapi
import os

# Create logger
logger = logging.getLogger("__main__.instagram_handler")

def log_in_to_instagram():
    logger.info("Log in to Instagram")
    cl = instagrapi.Client()
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    cl.login(username, password)

    return cl, username

def get_latest_posts(cl, username):
    # Get id from Instagram username
    user_id = cl.user_id_from_username(username)
    
    logger.info("Getting last 10 posts from Instagram...")
    latest_posts = cl.user_medias(user_id, 10)
    
    logger.info("Sorting Instagram posts by date")
    latest_posts_sorted = sorted(latest_posts, key=lambda post: post.taken_at)

    return latest_posts_sorted