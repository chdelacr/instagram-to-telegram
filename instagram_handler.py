from datetime import datetime

def get_latest_posts(cl, username):
    print("Getting id from Instagram username...")
    user_id = cl.user_id_from_username(username)
    
    print("Getting last 10 posts from Instagram...")
    latest_posts = cl.user_medias(user_id, 10)

    print("Sorting posts by date...")
    latest_posts_sorted = sorted(latest_posts, key=lambda post: post.taken_at)

    return latest_posts_sorted