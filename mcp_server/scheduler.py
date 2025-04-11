# mcp_server/scheduler.py
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from mcp_server.core.summarizer import summarize_posts
from mcp_server.core.slack_notifiers import send_pdf_to_slack
from mcp_server.tools.reddit_digest.tool import handle
from mcp_server.tools.reddit_digest.reddit_fetcher import fetch_subreddit_posts
from mcp_server.tools.reddit_digest.markdown_generator import generate_markdown
from mcp_server.tools.reddit_digest.pdf_generator import save_pdf_from_markdown
from mcp_server.tools.reddit_digest.markdown_generator import generate_markdown
from mcp_server.tools.reddit_digest.reddit_fetcher import fetch_from_subreddits
import logging
import os

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Slack token and channel ID from env
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL_ID")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger.info(f"SLACK_BOT_TOKEN: {bool(SLACK_BOT_TOKEN)} | SLACK_CHANNEL: {SLACK_CHANNEL}")

def scheduled_reddit_digest():
    try:
        topic = "ai, IndiaTech, programming"
        logger.info(f"[{datetime.now()}] ⏰ Running scheduled digest for: {topic}")

        # Step 1: Fetch
        posts = fetch_from_subreddits(topic)  # ✅ Direct function call


        # Step 2: Summarize
        summaries = summarize_posts(posts)

        # Step 3: Generate digest
        markdown_text = generate_markdown(topic, summaries)
        _, pdf_path = save_pdf_from_markdown(markdown_text, topic)


        logger.info(f"✅ Digest generated: {pdf_path}")

        # Step 4: Notify
        if SLACK_BOT_TOKEN and SLACK_CHANNEL:
            send_pdf_to_slack(file_path=pdf_path, title="India vs Global Tech Digest", channel=SLACK_CHANNEL)
        else:
            logger.warning("⚠️ SLACK_BOT_TOKEN or SLACK_CHANNEL_ID not set. Skipping Slack upload.")

    except Exception as e:
        logger.error(f"❌ Scheduled digest failed: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_reddit_digest, 'interval', minutes=1)  # for testing
    #scheduler.add_job(scheduled_reddit_digest, 'cron', hour=9, minute=0)
    scheduler.start()
    logger.info("🧪 Scheduler started with 1-minute interval for testing.")
