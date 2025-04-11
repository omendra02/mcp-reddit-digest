# mcp_server/main.py
from mcp_server.scheduler import start_scheduler
from fastapi import FastAPI
from pydantic import BaseModel
from mcp_server.tools import hello_tool
from mcp_server.tools.reddit_digest import reddit_tool
from mcp_server.core.summarizer import summarize_posts
from mcp_server.core.slack_notifiers import send_pdf_to_slack
from mcp_server.tools.reddit_digest.tool import handle
from dotenv import load_dotenv
load_dotenv()


#import logging
#logging.basicConfig(level=logging.DEBUG) for testing logging

# Initialize the FastAPI app
app = FastAPI()

start_scheduler() #for cron jobs

@app.get("/")
def root():
    return {"message": "MCP Reddit Digest Server Running"}


class MCPRequest(BaseModel):
    input: str  # Example: "ai", "cybersecurity", "tech update"

@app.post("/mcp/hello")
async def mcp_hello(req: MCPRequest):
    return {"output": hello_tool.handle(req.input)}

@app.post("/mcp/reddit")
async def mcp_reddit(req: MCPRequest):
    topic = req.input.strip().lower()

    # Step 1: Fetch posts for the topic
    posts = reddit_tool.fetch_subreddit_posts(topic=topic)

    # Step 2: Summarize them using OpenAI (from openai_summarizer)
    summaries = summarize_posts(posts)

    # Step 3: Generate Markdown + PDF digest
    markdown_text, pdf_path = reddit_tool.generate_digest(topic, summaries)

    # Step 4: Send PDF to Slack
    send_pdf_to_slack(pdf_path, title=f"Reddit Digest: {topic}")

    return {
        "output": f"✅ Digest generated for topic: *{topic}*\n\n{markdown_text}",
        "pdf_path": pdf_path
    }


@app.post("/mcp/reddit/subreddit")
async def mcp_custom_subreddits(req: MCPRequest):
    subreddit_input = req.input.strip()

    # 1. Fetch top posts from each subreddit
    posts = reddit_tool.fetch_from_subreddits(subreddit_input)

    # 2. Summarize
    summaries = summarize_posts(posts)

    # 3. Generate digest
    markdown_text, pdf_path = reddit_tool.generate_digest(subreddit_input, summaries)

    # 4. Send PDF to Slack
    send_pdf_to_slack(pdf_path, title=f"Reddit Digest: {subreddit_input}")

    return {
        "output": f"✅ Digest generated for subreddits: *{subreddit_input}*\n\n{markdown_text}",
        "pdf_path": pdf_path
    }
