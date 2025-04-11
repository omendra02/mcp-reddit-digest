# mcp_server/tools/tests/test_send_pdf_to_slack.py

import os
from dotenv import load_dotenv

# ✅ Load the .env file manually from the root
load_dotenv()

from mcp_server.core.slack_notifiers import send_pdf_to_slack

# Provide a valid test PDF path here
pdf_path = "output/reddit_digest_ai, IndiaTech, programming_20250411.pdf"

# Optional: Debug print to confirm env variable is loaded
print("SLACK_CHANNEL:", os.getenv("SLACK_CHANNEL"))

# Call function to test PDF send
send_pdf_to_slack(pdf_path)
