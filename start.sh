#!/bin/bash

# Download NLTK punkt data to a known location
python3 -m nltk.downloader punkt -d /app/nltk_data

# Set environment variable so Sumy can find the data
export NLTK_DATA=/app/nltk_data

# Run the bot
python3 main.py
