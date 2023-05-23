# Instagram posts to Telegram channel
Send your latest Instagram posts to your Telegram channel with instagrapi and a Telegram bot.

## Features
- Shares pictures, albums and videos
- Optional login to pull private posts
- Only shares posts that have not been shared
- Use of SFTP for creating checkpoint files
- Uses secrets as environment variables
- Runs with GitHub Actions

## Prerequisites
- Defining GitHub Secrets as environment variables
- Python 3.11+ (for local run)
- Telegram bot (follow the [guide](https://core.telegram.org/bots/features#creating-a-new-bot))
- Instagram account (optional login, but required when pulling public data fails)

## Getting started
Customize the configuration by setting up the required parameters, either in GitHub Secrets or the `.env` file:

| Parameter             | Description                                                                                                                                                                                            |
|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `INSTAGRAM_USERNAME`  | Your Instagram username                                                                                                                                                                                |
| `INSTAGRAM_PASSWORD`  | Your Instagram password (optional)                                                                                                                                                                     |
| `TELEGRAM_BOT_TOKEN`  | Your Telegram bot token (use [BotFather](http://t.me/botfather) to create your bot by following this [guide](https://core.telegram.org/bots/features#creating-a-new-bot))                              |
| `TELEGRAM_CHANNEL_ID` | Your Telegram channel ID (if public, `@channel_name`; if private, forward a message from the channel to [GetIDs Bot](http://t.me/getidsbot) and use the ID from "Origin chat" that starts with `-100`)|
| `SFTP_SERVER`         | Your SFTP server                                                                                                                                                                                       |
| `SFTP_USERNAME`       | Your SFTP username                                                                                                                                                                                     |
| `SFTP_PASSWORD`       | Your SFTP password                                                                                                                                                                                     |
| `SFTP_PATH`           | Your SFTP path                                                                                                                                                                                         |

Please note that `PRIVATE_ACCESS` is set by default to `"N"` in the `.env` file.

### Running with GitHub Actions
1. Fork the repo
2. Open your repo settings
3. Go to _**"Security > Secrets and variables > Actions"**_
4. Create and define your [parameters](https://github.com/chdelacr/instagram-to-telegram#getting-started) with the button _**"New repository secret"**_
5. Push any change to the `main` branch to trigger the job

Due to limitations with GitHub Actions, jobs are executed every 6 hours, and in-progress jobs are canceled if a new job is executed before that.

### Running locally
1. Clone the repository and navigate to the project directory:
    ```shell
    git clone https://github.com/chdelacr/instagram-to-telegram.git
    cd instagram-to-telegram
    ```
2. Update the `.env` file with your [parameters](https://github.com/chdelacr/instagram-to-telegram#getting-started) between double quotes (`""`)
2. Create and activate a virtual environment:
    ```shell
    python -m venv venv

    # Linux and macOS:
    source venv/bin/activate

    # Windows:
    venv\Scripts\activate
    ```
3. Install dependencies:
    ```shell
    pip install -r requirements.txt
    ```
4. Run the job:
    ```shell
    python main.py
    ```

## Credits
- [instagrapi](https://adw0rd.github.io/instagrapi/)
- [python-telegram-bot](https://python-telegram-bot.org/)

## Disclaimer
This is a personal project and is not affiliated with Instagram or Telegram in any way.
