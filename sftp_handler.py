import logging
import os
import pysftp
from datetime import datetime, timedelta

# Create logger
logger = logging.getLogger("__main__.sftp_handler")

def get_sftp_credentials():
    # SFTP credentials
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    sftp_server = os.getenv("SFTP_SERVER")
    sftp_username = os.getenv("SFTP_USERNAME")
    sftp_password = os.getenv("SFTP_PASSWORD")
    sftp_path = os.getenv("SFTP_PATH")
    
    return cnopts, sftp_server, sftp_username, sftp_password, sftp_path

def sftp_instagram_dump(operation):
    cnopts, sftp_server, sftp_username, sftp_password, sftp_path = get_sftp_credentials()
    
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        with sftp.cd(sftp_path):
            if operation == 'l':
                logger.info("Loading dump settings from SFTP")
                sftp.get("remote_dump.json", "local_dump.json")
            elif operation == 'c':
                logger.info("Copying dump settings to SFTP")
                sftp.put("local_dump.json", "remote_dump.json")
        sftp.close()
    
def sftp_checkpoint_utils(operation, new_posts = set()):
    cnopts, sftp_server, sftp_username, sftp_password, sftp_path = get_sftp_credentials()

    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    filename = f'sent_posts_{current_date}.txt'
    lookup_days = 7
    
    # Connect to SFTP server
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        if operation == 'r':
            with sftp.cd(sftp_path):
                # Look for latest checkpoint files
                for i in range(lookup_days):
                    filename = f'sent_posts_{(datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")}.txt'
                    if sftp.exists(filename):
                        logger.info("Reading checkpoint file in SFTP server")
                        with sftp.open(filename, 'r') as f:
                            sent_posts = set([line.strip() for line in f.readlines()])
                        break
                    elif (datetime.utcnow() - timedelta(days=lookup_days)) > datetime.strptime(filename.split("_")[-1].split(".")[0], '%Y-%m-%d'):
                        break
                else:
                    sent_posts = set()
            return sent_posts
        elif operation == 'w':
            if new_posts:
                with sftp.cd(sftp_path):
                    logger.info("Updating checkpoint file in SFTP server")
                    with sftp.open(filename, 'a') as f:
                        f.write('\n'.join(new_posts))
                        f.write('\n')
            else:
                logger.info("No new Instagram posts")
        elif operation == 'd':
            with sftp.cd(sftp_path):
                for file in sftp.listdir():
                    if file.startswith('sent_posts_'):
                        mtime = sftp.stat(file).st_mtime
                        if (datetime.now() - datetime.fromtimestamp(mtime)).days > lookup_days:
                            logger.info(f"Deleting checkpoint files older than {lookup_days} days from SFTP server")
                            sftp.remove(file)
                        
        sftp.close()