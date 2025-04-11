from datetime import datetime


def shorten(text, max_words=60):
    words = text.split()
    return ' '.join(words[:max_words]) + ('...' if len(words) > max_words else '')

def generate_markdown(topic: str, summaries: list) -> str:
    date_str = datetime.now().strftime('%B %d, %Y')
    markdown_content = f"# 📰 Reddit Digest: *{topic.title()}*\n"
    markdown_content += f"📅 **Date:** {date_str}\n\n---\n"

    subreddit_map = {}

    for item in summaries:
        if isinstance(item, str) and item.startswith("["):
            end = item.find("]")
            subreddit = item[1:end] if end != -1 else "General"
            content = item[end+1:].strip()
        else:
            subreddit = "General"
            content = item

        subreddit_map.setdefault(subreddit, []).append(content)

    for subreddit, posts in subreddit_map.items():
        markdown_content += f"\n## 🔸 r/{subreddit}\n\n"
        for idx, summary in enumerate(posts, 1):
            markdown_content += f"**{idx}.** {shorten(summary)}\n\n"

    return markdown_content
