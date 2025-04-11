from openai import AzureOpenAI
from typing import List
import os

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def summarize_posts(posts: List[dict]) -> List[str]:
    """
    Summarizes a list of Reddit posts using Azure OpenAI.
    Each post will be summarized individually.
    """
    summaries = []

    for post in posts:
        try:
            text = f"Title: {post['title']}\n\nContent: {post['selftext']}"
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes Reddit posts."},
                    {"role": "user", "content": f"Summarize the following Reddit post:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=300
            )
            summary = response.choices[0].message.content.strip()
            summaries.append(f"[{post['subreddit']}] {summary}")
        except Exception as e:
            summaries.append(f"[{post['subreddit']}] ❌ Error summarizing post: {str(e)}")

    return summaries
