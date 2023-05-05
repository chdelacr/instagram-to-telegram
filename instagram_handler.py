import logging

# Create logger
logger = logging.getLogger("__main__.instagram_handler")

def get_latest_posts(cl, username):
    # Get id from Instagram username
    user_id = cl.user_id_from_username(username)
    
    logger.info("Getting last 10 posts from Instagram...")
    latest_posts = cl.user_medias(user_id, 10)
    
    logger.info("Sorting Instagram posts by date")
    latest_posts_sorted = sorted(latest_posts, key=lambda post: post.taken_at)

    return latest_posts_sorted