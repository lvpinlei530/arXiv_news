import os
import dotenv
import requests
import json
from datetime import datetime, timedelta

SEVEN_DAYS_EARLIER = datetime.now() + timedelta(days=1) - timedelta(days=7)
START_DATE = SEVEN_DAYS_EARLIER.strftime('%Y%m%d0600')
TOMORROW = datetime.now() + timedelta(days=1)
END_DATE = TOMORROW.strftime('%Y%m%d0600')
DATE_RANGE = f"{START_DATE} TO {END_DATE}"


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
ENV_PATH = os.path.join(PROJECT_ROOT, "config", ".env")
CONFIG_FILE = os.path.join(PROJECT_ROOT, "config", "config.json")
DB_PATH = os.path.join(PROJECT_ROOT, "data", "local_database.db")
DB_LINK = f'sqlite:///{DB_PATH}'


def send_slack_message(
        message,
        channel,
        slack_url=None,
        display_name="ANT",
        timeout=60,
        icon_emoji=":ant:",
):  # channel='@chen') # for testing - your QCI email username?
    try:
        print(message)  # echo to Pyqumen user's console output?
        if slack_url is None:
            dotenv.load_dotenv(ENV_PATH)
            slack_url = os.getenv("SLACK_URL")
        webhook_url = rf'{slack_url}'
        payload = {
            "channel": channel,
            "icon_emoji": icon_emoji,
            "text": message,
            "username": display_name,
        }
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            timeout=timeout,  # just in case this is is blocking other scripts
            headers={"Content-Type": "application/json"},
        )
        print(response)
        return response
    except Exception as e:
        error_message = "could not send Slack message - {}".format(e)
        print(error_message)
        return
