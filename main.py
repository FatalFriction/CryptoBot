import requests
import html
import logging
import asyncio
from telegram import Bot
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer as SumyTokenizer
from sumy.summarizers.lsa import LsaSummarizer
from deep_translator import GoogleTranslator
import nltk
from nltk import data as nltk_data
from datetime import datetime, time as dtime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()

# === Setup NLTK Data Path ===
nltk_data_path = "/app/nltk_data"
os.makedirs(nltk_data_path, exist_ok=True)
os.environ["NLTK_DATA"] = nltk_data_path
nltk_data.path.append(nltk_data_path)
nltk.download("punkt", download_dir=nltk_data_path, quiet=True)

# === Summarizer ===
def summarize_text(text, sentence_count=6):
    parser = PlaintextParser.from_string(text, SumyTokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in summary)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
COINDESK_API_URL = os.getenv("COINDESK_API_URL")
API_KEY = os.getenv("API_KEY")

# === Setup ===
logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)

bot = Bot(token=TELEGRAM_API_TOKEN)

# Store already sent URLs to avoid duplicates
sent_urls = set()

# === Fetcher ===
async def fetch_latest_news():
    logging.info("Fetching latest news from Coindesk...")
    try:
        headers = {'Authorization': f'Bearer {API_KEY}'}
        response = requests.get(COINDESK_API_URL, headers=headers)

        if response.status_code != 200:
            logging.error(f"Error {response.status_code}: {response.text}")
            return []

        news_data = response.json()
        articles = news_data.get("Data", [])
        logging.info(f"Fetched {len(articles)} articles.")
        return articles if isinstance(articles, list) else []

    except requests.exceptions.RequestException:
        logging.exception("Network error while fetching articles.")
    except Exception:
        logging.exception("Unexpected error while parsing article data.")
    return []

# === Sender ===
async def send_article(article):
    try:
        url = article.get("URL", "")
        if url in sent_urls:
            logging.info(f"Skipped duplicate article: {url}")
            return

        title = html.escape(article.get("TITLE", "No Title"))
        body = article.get("BODY", "")
        sentiment = html.escape(article.get("SENTIMENT", ""))
        image_url = article.get("IMAGE_URL", "")
        categories = article.get("CATEGORY_DATA", [])
        coin_names = html.escape(" ".join(f"#{(cat.get('CATEGORY', ''))}" for cat in categories if cat.get('CATEGORY')))
        summary = html.escape(summarize_text(body))
        source_name = html.escape(article.get("SOURCE_DATA", {}).get("NAME", "Unknown Source"))
        source_link = f'<a href="{url}">{source_name}</a>'
        
        # Translate to Bahasa Indonesia
        title = GoogleTranslator(source='auto', target='id').translate(title)
        summary = GoogleTranslator(source='auto', target='id').translate(summary)
        sentiment = GoogleTranslator(source='auto', target='id').translate(sentiment)

        message = (
            f"📰 <b>{title}</b>\n\n"
            f"{summary}\n\n"
            f"🧠 Sentiment Crypto Market {sentiment.capitalize()}\n"
            f"📡 Sumber {source_link}\n\n"
            f'Untuk yang belum pakai MEXC bisa pakai link official partnership kita di sini tinggal klik <a href="https://www.mexc.com/register?inviteCode=mexc-12Hnph">Register</a> atau via Link Alternatif <a href="https://promote.mexc.com/a/CVWtpYro">Register</a> lalu selesaikan pengisian Dokumen-nya\n\n'
            f"{coin_names}\n\n@kriptorakyat"
        )

        await bot.send_message(
                chat_id=CHAT_ID,
                text=message,
                parse_mode="HTML"
            )

        sent_urls.add(url)

    except Exception as e:
        logging.exception(f"Error sending article: {e}")

# === Async Queues ===
async def fetch_loop(queue: asyncio.Queue):
    while True:
        articles = await fetch_latest_news()
        for article in articles:
            url = article.get("URL", "")
            if url and url not in sent_urls:
                await queue.put(article)
        logging.info("Sleeping 30 minutes before next fetch...")
        await asyncio.sleep(1800)

# Set timezone to UTC+7
timezone = pytz.timezone("Asia/Bangkok")

def is_within_allowed_hours():
    now = datetime.now(timezone).time()
    start = dtime(6, 0)
    end = dtime(23, 59, 59)
    return start <= now <= end or dtime(0, 0) <= now <= dtime(1, 0)

async def send_loop(queue: asyncio.Queue):
    while True:
        if is_within_allowed_hours():
            if not queue.empty():
                article = await queue.get()
                await send_article(article)
            else:
                logging.info("Queue is empty. Nothing to send.")
        else:
            logging.info("Outside allowed hours. Skipping send.")

        logging.info("Sleeping 2 hours before sending next article...")
        await asyncio.sleep(7200)

# === Run ===
async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        fetch_loop(queue),
        send_loop(queue)
    )

if __name__ == "__main__":
    asyncio.run(main())
