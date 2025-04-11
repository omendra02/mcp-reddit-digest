import os
from markdown2 import markdown
from weasyprint import HTML, CSS
from datetime import datetime
from mcp_server.tools.reddit_digest.markdown_generator import generate_markdown
from mcp_server.tools.reddit_digest.reddit_fetcher import fetch_subreddit_posts
from mcp_server.core.summarizer import summarize_posts

def save_pdf_from_markdown(markdown_text: str, topic: str):
    date_str = datetime.now().strftime('%Y%m%d')
    filename_base = f"reddit_digest_{topic}_{date_str}"
    md_path = f"{filename_base}.md"
    pdf_path = f"{filename_base}.pdf"

    with open(md_path, "w") as f:
        f.write(markdown_text)

    html_content = markdown(markdown_text)
    css_path = os.path.join(os.path.dirname(__file__), "style.css")

    if os.path.exists(css_path):
        HTML(string=html_content).write_pdf(pdf_path, stylesheets=[CSS(css_path)])
    else:
        HTML(string=html_content).write_pdf(pdf_path)

    return md_path, pdf_path
