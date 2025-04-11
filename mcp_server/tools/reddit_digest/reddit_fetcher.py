import os
import praw
from dotenv import load_dotenv


load_dotenv()

def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("USER_AGENT")
    )

TOPIC_SUBREDDITS = {
    "tech update": ["technology", "technews", "IndiaTech", "developersIndia"],
    "ai": ["MachineLearning", "ArtificialIntelligence", "Singularity", "artificial"],
    "cybersecurity": ["cybersecurity", "netsec", "Malware"],
    "programming": ["programming", "learnprogramming", "java", "Python"],
    "startups": ["startups", "Entrepreneur", "startup"],
}

def fetch_subreddit_posts(topic="tech update"):
    reddit = get_reddit_instance()
    subreddits = TOPIC_SUBREDDITS.get(topic.lower(), ["technology", "technews"])

    posts = []
    for sub in subreddits:
        for post in reddit.subreddit(sub).hot(limit=5):
            posts.append({
                "subreddit": sub,
                "title": post.title,
                "url": post.url,
                "selftext": (post.selftext or "")[:500]
            })
    return posts

def fetch_from_subreddits(subreddit_input: str):
    reddit = get_reddit_instance()
    subreddits = [sub.strip() for sub in subreddit_input.split(",") if sub.strip()]

    posts = []
    for sub in subreddits:
        try:
            for post in reddit.subreddit(sub).hot(limit=5):
                posts.append({
                    "subreddit": sub,
                    "title": post.title,
                    "url": post.url,
                    "selftext": (post.selftext or "")[:500]
                })
        except Exception as e:
            posts.append({
                "subreddit": sub,
                "title": "Fetch Error",
                "url": "",
                "selftext": f"Could not fetch posts from r/{sub}: {str(e)}"
            })
    return posts
