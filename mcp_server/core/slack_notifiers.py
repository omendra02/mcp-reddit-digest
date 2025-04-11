import os
import logging
from typing import Optional
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from mcp_server.core.utils import resolve_slack_channel_id, file_exists
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DEFAULT_CHANNEL = os.getenv("SLACK_CHANNEL_ID")

client = WebClient(token=SLACK_BOT_TOKEN)


def send_message_to_slack(message: str, channel: Optional[str] = None) -> bool:
    if not SLACK_BOT_TOKEN:
        logger.error("❌ Slack token not set in environment variables.")
        return False

    channel = resolve_slack_channel_id(client, channel or DEFAULT_CHANNEL)
    if not channel:
        return False

    try:
        response = client.chat_postMessage(channel=channel, text=message)
        logger.info(f"✅ Sent message to Slack: {response['ts']}")
        return True
    except SlackApiError as e:
        logger.error(f"❌ Slack API error: {e.response['error']}")
    except Exception as e:
        logger.error(f"❌ Failed to send message to Slack: {e}")
    return False


def send_pdf_to_slack(file_path: str, title: str = "Daily Reddit Digest", channel: Optional[str] = None) -> bool:
    if not SLACK_BOT_TOKEN:
        logger.error("❌ Slack token not set in environment variables.")
        return False

    if not file_exists(file_path):
        logger.error(f"❌ File does not exist: {file_path}")
        return False

    channel = resolve_slack_channel_id(client, channel or DEFAULT_CHANNEL)
    if not channel:
        return False

    try:
        logger.info(f"📡 Using Slack channel: {channel}")
        response = client.files_upload_v2(
            file=file_path,
            title=title,
            channel=channel,
            initial_comment="📄 Here's your daily tech digest!"
        )
        logger.info("✅ PDF uploaded and posted to Slack.")
        return True

    except SlackApiError as e:
        logger.error(f"❌ Slack API error: {e.response['error']}")
    except Exception as e:
        logger.error(f"❌ Failed to upload file to Slack: {e}")
    return False

