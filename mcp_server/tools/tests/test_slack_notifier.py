from dotenv import load_dotenv

# Load the .env file from project root
load_dotenv()


from mcp_server.core.slack_notifiers import send_message_to_slack

send_message_to_slack("Hey! This is a test from MCP Slack notifier.")
