from instagram import get_new_posts
from telegram import send_posts_to_channel
import time

while True:
    # Obtener nuevas publicaciones de Instagram
    new_posts = get_new_posts()

    # Enviar nuevas publicaciones al canal de Telegram
    send_posts_to_channel(new_posts)

    # Esperar 1 minuto antes de volver a comprobar nuevas publicaciones
    time.sleep(60)
