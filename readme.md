# 📰 Crypto News Telegram Bot

This bot fetches the latest crypto news from the Coindesk API, summarizes the articles using LSA summarization, translates them into Bahasa Indonesia using Google Translate, and sends the result to a Telegram group or channel.

## Features

- Summarizes news with LSA algorithm
- Translates to Bahasa Indonesia
- Sends formatted messages via Telegram bot
- Filters out duplicate articles
- Only sends during specific hours (06:00–01:00 UTC+7)

## Environment Variables

Create a `.env` file and define the following:

```env
TELEGRAM_API_TOKEN=your_bot_token
CHAT_ID=your_group_or_channel_id
COINDESK_API_URL=https://your-coindesk-endpoint.com
API_KEY=your_coindesk_api_key
