def get_latest_posts(cl, username):
    print("Getting id from Instagram username...")
    user_id = cl.user_id_from_username(username)
    
    print("Getting last 10 posts from Instagram account...")
    posts = cl.user_medias(user_id, 10)

    return posts