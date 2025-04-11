from mcp_server.tools.reddit_digest.reddit_fetcher import fetch_subreddit_posts
from mcp_server.core.summarizer import summarize_posts
from mcp_server.tools.reddit_digest.markdown_generator import generate_markdown
from mcp_server.tools.reddit_digest.pdf_generator import save_pdf_from_markdown

def handle(topic="tech update"):
    posts = fetch_subreddit_posts(topic)
    summaries = summarize_posts(posts)
    markdown_text = generate_markdown(topic, summaries)
    _, pdf_path = save_pdf_from_markdown(markdown_text, topic)
    return {
        "topic": topic,
        "summary": markdown_text,
        "pdf": pdf_path
    }
