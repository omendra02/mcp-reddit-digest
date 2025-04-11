# 🧠 MCP Reddit Digest Server

A FastAPI-based MCP (Model Context Protocol) server tool that fetches top Reddit posts from selected subreddits, summarizes them using Azure OpenAI, and generates a daily PDF digest in Markdown style. The digest is automatically uploaded to a Slack channel.

## ✨ Features

- 🔍 Fetches top Reddit posts based on predefined topics or custom subreddit input
- 🧠 Summarizes content using Azure OpenAI
- 📝 Generates a clean Markdown digest
- 📄 Converts Markdown to PDF with custom styling
- 🔁 Supports scheduled digests using APScheduler with cron expressions
- 📬 Uploads generated PDF to a Slack channel
- 🧩 Modular MCP tool architecture for easy extensibility
