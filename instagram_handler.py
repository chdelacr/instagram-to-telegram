import instagrapi
import os

def get_new_posts():
    print("Login into Instagram...")
    cl = instagrapi.Client()
    username = os.environ['INSTAGRAM_USERNAME']
    password = os.environ['INSTAGRAM_PASSWORD']
    cl.login(username, password)
    
    print("Getting id from Instagram username...")
    user_id = cl.user_id_from_username(username)
    
    print("Getting last 10 posts from Instagram account...")
    return cl.user_medias(user_id, 10)