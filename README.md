# MCP Reddit Digest Server

A FastAPI-based MCP (Model Context Protocol) server that automatically fetches, summarizes, and delivers Reddit content directly to Slack. The system uses Azure OpenAI to create concise summaries of top posts from selected subreddits, formats them into organized PDF reports, and shares them with your team.

## ✨ Features

- 🔍 **Smart Reddit Monitoring**: Fetch top posts by topic (AI, cybersecurity, programming) or specify custom subreddits
- 🧠 **AI-Powered Summaries**: Condense lengthy Reddit discussions using Azure OpenAI
- 📝 **Clean Markdown Formatting**: Generate well-structured digests with posts organized by subreddit
- 📄 **Professional PDF Reports**: Convert markdown to styled PDFs with custom CSS
- 🔔 **Slack Integration**: Automatically deliver digests to your team's Slack channels
- ⏱️ **Scheduled Delivery**: Configure automated digests on a daily or custom schedule
- 🧩 **Modular Architecture**: Easily extend with new features or integrations

## Certified by MCPHub : [Reddit Digest - omendra02 MCP Server](https://mcphub.com/mcp-servers/omendra02/mcp-reddit-digest)

### Prerequisites

- Python 3.8+
- Reddit API credentials
- Azure OpenAI API access
- Slack workspace with bot integration

### Environment Setup

Create a `.env` file in the project root with the following variables:

```
# Reddit API
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
USER_AGENT=your_user_agent

# Azure OpenAI
AZURE_OPENAI_KEY=your_openai_key
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT=your_deployment_name

# Slack
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_CHANNEL_ID=your_channel_id
```

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-reddit-digest.git
cd mcp-reddit-digest

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn mcp_server.main:app --reload
```

## 🔧 Usage

### API Endpoints

- `GET /` - Health check endpoint
- `POST /mcp/hello` - Test endpoint for verifying connectivity
- `POST /mcp/reddit` - Generate digests by topic (ai, cybersecurity, tech update, etc.)
- `POST /mcp/reddit/subreddit` - Generate digests from custom subreddits

### Example Requests

#### Generate a digest by topic:
```bash
curl -X POST "http://localhost:8000/mcp/reddit" \
  -H "Content-Type: application/json" \
  -d '{"input": "ai"}'
```

#### Generate a digest for specific subreddits:
```bash
curl -X POST "http://localhost:8000/mcp/reddit/subreddit" \
  -H "Content-Type: application/json" \
  -d '{"input": "MachineLearning, artificial, IndiaTech"}'
```

## ⚙️ Configuration

### Scheduled Digests

The system is configured to run scheduled digests. Edit `scheduler.py` to adjust the timing:

```python
# For production (runs daily at 9 AM)
scheduler.add_job(scheduled_reddit_digest, 'cron', hour=9, minute=0)

# For testing (runs every minute)
scheduler.add_job(scheduled_reddit_digest, 'interval', minutes=1)
```

### Topic Mappings

Default topic-to-subreddit mappings are defined in `reddit_fetcher.py`. Add or modify mappings as needed:

```python
TOPIC_SUBREDDITS = {
    "tech update": ["technology", "technews", "IndiaTech", "developersIndia"],
    "ai": ["MachineLearning", "ArtificialIntelligence", "Singularity", "artificial"],
    # Add new mappings here
}
```

## 🔄 Project Structure

```
mcp_server/
├── core/
│   ├── slack_notifiers.py    # Slack integration
│   ├── summarizer.py         # Azure OpenAI integration
│   └── utils.py              # Helper functions
├── tools/
│   ├── hello_tool.py         # Simple test tool
│   └── reddit_digest/        # Reddit digest functionality
│       ├── markdown_generator.py
│       ├── pdf_generator.py
│       ├── reddit_fetcher.py
│       ├── style.css         # PDF styling
│       └── tool.py           # Main digest logic
├── main.py                   # FastAPI application
├── mcp.json                  # Tool definitions
└── scheduler.py              # Automated tasks
```
