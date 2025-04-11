import os
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


def resolve_slack_channel_id(client: WebClient, channel: str) -> str:
    """
    Resolves Slack channel name (e.g., #general) to channel ID.
    If already ID, returns as-is.
    """
    if not channel:
        logger.error("❌ Slack channel ID or name not provided.")
        return ""

    if channel.startswith("C"):  # Already a channel ID
        return channel

    if channel.startswith("#"):
        channel_name = channel.lstrip("#")
        try:
            result = client.conversations_list(types="public_channel,private_channel", limit=1000)
            channels = result.get("channels", [])
            match = next((c for c in channels if c["name"] == channel_name), None)
            if match:
                return match["id"]
            logger.error(f"❌ Channel #{channel_name} not found.")
        except SlackApiError as e:
            logger.error(f"❌ Failed to resolve channel ID: {e.response['error']}")
    return ""


def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)
