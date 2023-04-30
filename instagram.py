import instaloader
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

def get_new_posts():
    # Iniciar sesión en Instagram
    L = instaloader.Instaloader()
    L.context.log("Inicio de sesión en Instagram...")
    L.load_session_from_file(INSTAGRAM_USERNAME)
    if not L.context.is_logged_in:
        L.context.log("No se pudo iniciar sesión en Instagram.")
        return []

    # Obtener el perfil de Instagram
    profile = instaloader.Profile.from_username(L.context, INSTAGRAM_USERNAME)

    # Obtener las nuevas publicaciones
    new_posts = []
    for post in profile.get_posts():
        if post.date_local > profile.last_post.date_local:
            new_posts.append(post)
    profile.last_post = profile.get_posts()[0]

    return new_posts
