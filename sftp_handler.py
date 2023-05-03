import os
import pysftp
from datetime import datetime
    
def sftp_utils(operation, sent_posts = set()):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    sftp_server = os.getenv("SFTP_SERVER")
    sftp_username = os.getenv("SFTP_USERNAME")
    sftp_password = os.getenv("SFTP_PASSWORD")
    sftp_path = os.getenv("SFTP_PATH")

    current_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'sent_posts_{current_date}.txt'
    
    # Connect to SFTP server
    with pysftp.Connection(sftp_server, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
        if operation == 'r':
            with sftp.cd(sftp_path):
                if sftp.exists(filename):
                    print("Reading checkpoint file...")
                    with sftp.open(filename, 'r') as f:
                        sent_posts = set([line.strip() for line in f.readlines()])
                        
            return sent_posts
        elif operation == 'w':
            with sftp.cd(sftp_path):
                print("Writing checkpoint file...")
                with sftp.open(filename, 'w') as f:
                    f.write('\n'.join(sent_posts))
        elif operation == 'd':
            for file in sftp.listdir():
                if file.startswith('sent_posts_'):
                    file_path = f'{sftp_path}/{file}'
                    mtime = sftp.stat(file_path).st_mtime
                    if (datetime.now() - datetime.fromtimestamp(mtime)).days > 7:
                        print("Deleting checkpoint files older than 7 days...")
                        sftp.remove(file_path)